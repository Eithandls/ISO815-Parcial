using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

// Configurar puerto explícito 5050 para evitar conflicto con Flask (5000)
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenLocalhost(5050);
});

var app = builder.Build();

// Lista en memoria de asientos contables recibidos
var asientos = new List<AsientoContable>
{
    new AsientoContable
    {
        Id = 1,
        Fecha = DateTime.Now.AddDays(-2).ToString("yyyy-MM-dd HH:mm:ss"),
        Descripcion = "Asiento inicial de inventario - Apertura",
        CuentaDebito = "1110-01",
        CuentaCredito = "2110-01",
        Monto = 3100.00m,
        Estado = "Contabilizado",
        ModuloOrigen = "Inventario (Flask ISO815)"
    }
};

// Endpoint GET: Estado del servicio de contabilidad
app.MapGet("/", () => Results.Ok(new
{
    Servicio = "Web Service de Contabilidad - ISO815",
    Tecnologia = "C# / ASP.NET Core (.NET 11)",
    Estado = "Activo y en escucha",
    Puerto = 5050,
    TotalAsientos = asientos.Count,
    Documentacion = "Recibe asientos contables generados por transacciones de inventario desde Flask (Python)"
}));

// Endpoint GET: Consultar todos los asientos contables registrados
app.MapGet("/api/contabilidad/asientos", () => Results.Ok(asientos));

// Endpoint POST: Recibir asiento contable desde el sistema de inventario (Flask)
app.MapPost("/api/contabilidad/asientos", (AsientoRequest request) =>
{
    if (request.Monto <= 0)
    {
        return Results.BadRequest(new { Exito = false, Mensaje = "El monto del asiento debe ser mayor que cero." });
    }

    if (string.IsNullOrWhiteSpace(request.CuentaDebito) || string.IsNullOrWhiteSpace(request.CuentaCredito))
    {
        return Results.BadRequest(new { Exito = false, Mensaje = "Las cuentas contables débito y crédito son obligatorias." });
    }

    var nuevoAsiento = new AsientoContable
    {
        Id = asientos.Count + 1,
        Fecha = string.IsNullOrWhiteSpace(request.Fecha) ? DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") : request.Fecha,
        Descripcion = request.Descripcion ?? "Movimiento de inventario",
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
        Mensaje = "Asiento contable recibido y procesado exitosamente por el Web Service C#/.NET",
        Asiento = nuevoAsiento
    });
});

app.Run();

// Modelos de datos
public class AsientoContable
{
    public int Id { get; set; }
    public string Fecha { get; set; } = string.Empty;
    public string Descripcion { get; set; } = string.Empty;
    public string CuentaDebito { get; set; } = string.Empty;
    public string CuentaCredito { get; set; } = string.Empty;
    public decimal Monto { get; set; }
    public string Estado { get; set; } = "Contabilizado";
    public string ModuloOrigen { get; set; } = "Inventario";
}

public class AsientoRequest
{
    public string? Fecha { get; set; }
    public string? Descripcion { get; set; }
    public string? CuentaDebito { get; set; }
    public string? CuentaCredito { get; set; }
    public decimal Monto { get; set; }
}
