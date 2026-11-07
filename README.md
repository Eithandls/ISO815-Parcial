# Sistema de Gestión de Inventario (ISO815)

Proyecto final desarrollado para la asignatura **ISO815**. Corresponde a una solución académica para la administración, control y registro de movimientos de inventario bajo un esquema funcional y estructurado.

---

## Acceso al Sistema

Una vez iniciado el servidor local, el sistema se encuentra disponible en la siguiente dirección:

- **URL de acceso:** [http://localhost:5000](http://localhost:5000) (o `http://127.0.0.1:5000`)
- **Credenciales por defecto:**
  - **Usuario:** `admin`
  - **Contraseña:** `admin123`
  - **Rol:** Encargado de Insumos

---

## Arquitectura y Tecnologías

- **Lenguaje y Backend:** Python 3 con el microframework Flask.
- **Base de Datos:** SQLite (almacenamiento local mediante `inventario.db`, sin dependencia de servicios de base de datos externos).
- **Interfaz de Usuario:** HTML5, CSS3, JavaScript estándar y Bootstrap 5 para el diseño responsivo.

---

## Módulos del Sistema

### 1. Panel de Control (Dashboard)
- Indicadores cuantitativos del estado general del inventario: artículos activos, almacenes disponibles, tipos de inventario y transacciones registradas.
- Registro visual de los movimientos más recientes.

### 2. Gestión de Tipos de Inventario
- Catálogo para clasificar los artículos del sistema.
- Atributos: Identificador, Descripción, Cuenta Contable y Estado (Activo/Inactivo).
- Control de integridad referencial: restricción de eliminación si existen artículos vinculados.

### 3. Gestión de Artículos
- Operaciones CRUD completas para el catálogo de productos.
- Atributos: Identificador, Descripción, Existencia, Tipo de Inventario (clave foránea), Costo Unitario y Estado.
- Vista detallada del artículo junto con el historial de transacciones asociadas.

### 4. Gestión de Almacenes
- Administración de los depósitos o almacenes de la organización.
- Atributos: Identificador del Almacén, Descripción y Estado.
- Validación de dependencias antes de permitir la eliminación de registros.

### 5. Gestión de Transacciones
- Registro y control de movimientos de inventario en el mismo almacén:
  - **Entrada:** Incrementa las existencias del artículo en el almacén.
  - **Salida:** Reduce existencias del almacén previa validación de disponibilidad de stock.
  - **Ajuste:** Corrección directa de existencias en el sistema.
- Cálculo automático del monto total en función de la cantidad y el costo unitario.
- Mantenimiento de historial transaccional auditable.

---

## Instrucciones de Instalación y Ejecución

### Prerrequisitos
- Python versión 3.10 o superior instalado en el equipo y agregado a la variable de entorno `PATH`.

### Procedimiento

1. **Ubicarse en el directorio raíz del proyecto:**
   ```bash
   cd ISO815
   ```

2. **Instalar las dependencias requeridas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor de la aplicación:**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación:**
   Abra un navegador web e ingrese a [http://localhost:5000](http://localhost:5000).

*Nota: La base de datos y los datos de prueba iniciales se inicializan automáticamente en la primera ejecución si el archivo `inventario.db` no existe.*
