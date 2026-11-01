# 📦 Sistema de Gestión de Inventario (ISO815)

Proyecto final académico para la asignatura **ISO815**. Implementa los módulos de gestión y control de inventario con una interfaz sencilla, limpia y funcional.

---

## 🚀 Acceso Rápido

Cuando el servidor está en ejecución, accede al sistema en:

👉 **[http://localhost:5000](http://localhost:5000)** (o `http://127.0.0.1:5000`)

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3 + [Flask](https://flask.palletsprojects.com/)
- **Base de Datos:** SQLite (archivo local `inventario.db`, sin necesidad de servidores externos)
- **Frontend:** HTML5, CSS3, JavaScript puro y [Bootstrap 5](https://getbootstrap.com/) con [Bootstrap Icons](https://icons.getbootstrap.com/)

---

## 📋 Módulos Implementados

### 1. 📊 Dashboard
- Resumen con indicadores de artículos activos, almacenes activos, tipos de inventario y transacciones registradas.
- Visualización de los últimos movimientos realizados.

### 2. 🏷️ Tipos de Inventario
- Catálogo para clasificar artículos.
- Campos: Identificador, Descripción, Cuenta Contable y Estado (Activo/Inactivo).
- Validación de integridad referencial (no se elimina si tiene artículos asociados).

### 3. 📦 Artículos
- CRUD completo de productos.
- Campos: Identificador, Descripción, Existencia, Tipo de Inventario (FK), Costo Unitario y Estado.
- Vista de detalle con historial de transacciones asociadas al artículo.

### 4. 🏢 Almacenes
- Administración de almacenes o depósitos físicos.
- Campos: Identificador, Descripción y Estado.
- Validación referencial con movimientos existentes.

### 5. 🔄 Transacciones
- Registro de movimientos de inventario:
  - **Entrada:** Aumenta las existencias del artículo.
  - **Salida:** Disminuye las existencias (valida que haya stock suficiente).
  - **Traslado:** Registra movimiento entre almacén de origen y destino.
  - **Ajuste:** Corrección manual de existencias.
- Cálculo automático de montos según costo unitario.
- Historial completo de movimientos.

---

## ⚙️ Instalación y Ejecución

### Prerrequisitos
- Python 3.10 o superior instalado (marcar casilla *Add Python to PATH*).

### Pasos

1. **Clonar o ubicarse en la carpeta del proyecto:**
   ```bash
   cd ISO815
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   *(O directamente `pip install flask`)*

3. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

4. **Abrir en el navegador:**
   Navega a [http://localhost:5000](http://localhost:5000).

> 💡 **Nota:** La base de datos `inventario.db` y sus datos iniciales de demostración se crean automáticamente al iniciar la aplicación por primera vez.
