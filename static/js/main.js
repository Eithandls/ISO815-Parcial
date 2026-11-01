/**
 * ISO815 – main.js
 * Lógica JavaScript del frontend
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Formulario de Transacciones: mostrar/ocultar almacén destino ──
    const tipoSelect = document.getElementById('tipo');
    const campoDestino = document.getElementById('campo_almacen_destino');

    if (tipoSelect && campoDestino) {
        function toggleDestino() {
            if (tipoSelect.value === 'Traslado') {
                campoDestino.style.display = 'block';
                const selectDestino = campoDestino.querySelector('select');
                if (selectDestino) selectDestino.required = true;
            } else {
                campoDestino.style.display = 'none';
                const selectDestino = campoDestino.querySelector('select');
                if (selectDestino) {
                    selectDestino.required = false;
                    selectDestino.value = '';
                }
            }
        }
        tipoSelect.addEventListener('change', toggleDestino);
        toggleDestino(); // Ejecutar al cargar
    }

    // ── Auto-dismiss de alertas flash después de 4 segundos ──
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });

    // ── Actualizar monto en formulario de transacciones ──
    const articuloSelect = document.getElementById('id_articulo');
    const cantidadInput = document.getElementById('cantidad');
    const montoDisplay = document.getElementById('monto_calculado');

    // Costos por artículo inyectados desde el template via data-attribute
    function calcularMonto() {
        if (!articuloSelect || !cantidadInput || !montoDisplay) return;
        const option = articuloSelect.options[articuloSelect.selectedIndex];
        const costo = parseFloat(option ? option.dataset.costo || 0 : 0);
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const monto = (costo * cantidad).toFixed(2);
        montoDisplay.textContent = 'Monto estimado: $' + monto;
    }

    if (articuloSelect) articuloSelect.addEventListener('change', calcularMonto);
    if (cantidadInput) cantidadInput.addEventListener('input', calcularMonto);
});
