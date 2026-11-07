using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

// Configurar puerto explícito 5050 para evitar conflicto con Flask (5000)
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(5050);
});

var app = builder.Build();

// Variables de métricas y última comunicación
string? ultimaComunicacion = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
int totalErrores = 0;

// Lista en memoria de registros contables generados a partir de movimientos de inventario
var asientos = new List<AsientoContable>
{
    new AsientoContable
    {
        Id = 1,
        TransaccionId = 1,
        TipoMovimiento = "Entrada",
        Fecha = DateTime.Now.AddDays(-2).ToString("yyyy-MM-dd HH:mm:ss"),
        Descripcion = "Entrada inicial de insumos: Cuaderno Profesional 100 Hojas",
        CuentaDebito = "1110-01",
        CuentaCredito = "2110-01",
        Monto = 3100.00m,
        Estado = "Contabilizado",
        ModuloOrigen = "Inventario (Flask ISO815)"
    }
};

// Endpoint GET: Estado del servicio complementario de integración contable
app.MapGet("/", () =>
{
    return Results.Ok(new
    {
        Servicio = "Servicio de Integración Contable – C# / ASP.NET Core",
        Tecnologia = "C# / ASP.NET Core (.NET 11)",
        Estado = "Activo y en escucha",
        Puerto = 5050,
        TotalContabilizados = asientos.Count,
        TotalErrores = totalErrores,
        UltimaComunicacion = ultimaComunicacion,
        Descripcion = "Microservicio complementario que procesa los registros contables derivados de las entradas, salidas y ajustes del inventario."
    });
});

// Endpoint GET: Consultar los registros contables procesados
app.MapGet("/api/contabilidad/asientos", () =>
{
    ultimaComunicacion = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
    return Results.Ok(asientos);
});

// Endpoint POST: Recibir y procesar el impacto contable de un movimiento de inventario
app.MapPost("/api/contabilidad/asientos", (AsientoRequest request) =>
{
    ultimaComunicacion = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

    // Validación de monto
    if (request.Monto <= 0)
    {
        totalErrores++;
        return Results.BadRequest(new
        {
            Exito = false,
            Mensaje = "El importe contable debe ser mayor a cero."
        });
    }

    // Validación de cuentas contables
    if (string.IsNullOrWhiteSpace(request.CuentaDebito) || string.IsNullOrWhiteSpace(request.CuentaCredito))
    {
        totalErrores++;
        return Results.BadRequest(new
        {
            Exito = false,
            Mensaje = "Las cuentas contables de débito y crédito son obligatorias."
        });
    }

    // Prevención de registros duplicados por reenvío de una misma transacción de inventario
    if (request.TransaccionId.HasValue && request.TransaccionId.Value > 0)
    {
        var existente = asientos.FirstOrDefault(a => a.TransaccionId == request.TransaccionId.Value);
        if (existente != null)
        {
            return Results.Ok(new
            {
                Exito = true,
                Duplicado = true,
                Mensaje = $"La transacción #{request.TransaccionId.Value} ya fue procesada contablemente con el asiento #{existente.Id}.",
                Asiento = existente
            });
        }
    }

    var nuevoAsiento = new AsientoContable
    {
        Id = asientos.Count + 1,
        TransaccionId = request.TransaccionId ?? 0,
        TipoMovimiento = string.IsNullOrWhiteSpace(request.TipoMovimiento) ? "Movimiento" : request.TipoMovimiento,
        Fecha = string.IsNullOrWhiteSpace(request.Fecha) ? DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") : request.Fecha,
        Descripcion = request.Descripcion ?? "Operación de inventario",
        CuentaDebito = request.CuentaDebito,
        CuentaCredito = request.CuentaCredito,
        Monto = request.Monto,
        Estado = "Contabilizado",
        ModuloOrigen = "Inventario (Flask ISO815)"
    };

    asientos.Add(nuevoAsiento);

    return Results.Created($"/api/contabilidad/asientos/{nuevoAsiento.Id}", new
    {
        Exito = true,
        Duplicado = false,
        Mensaje = "Impacto contable registrado y procesado exitosamente por el servicio C#/.NET",
        Asiento = nuevoAsiento
    });
});

app.Run();

// Modelos de datos
public class AsientoContable
{
    public int Id { get; set; }
    public int TransaccionId { get; set; }
    public string TipoMovimiento { get; set; } = "Entrada";
    public string Fecha { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public string CuentaDebito { get; set; } = string.Empty;
    public string CuentaCredito { get; set; } = string.Empty;
    public decimal Monto { get; set; }
    public string Estado { get; set; } = "Contabilizado";
    public string ModuloOrigen { get; set; } = "Inventario (Flask ISO815)";
}

public class AsientoRequest
{
    public int? TransaccionId { get; set; }
    public string? TipoMovimiento { get; set; }
    public string? Fecha { get; set; }
    public string? Descripcion { get; set; }
    public string? CuentaDebito { get; set; }
    public string? CuentaCredito { get; set; }
    public decimal Monto { get; set; }
}
