# Sistema de Gestión de Inventario y Contabilidad (ISO815)

Proyecto final desarrollado para la asignatura **ISO815** y aplicable a la asignatura de **Tecnología Propietaria**. Implementa una arquitectura distribuida basada en microservicios e integración multiplataforma utilizando dos ecosistemas tecnológicos complementarios: **Python** y **C# / .NET**.

---

## Acceso al Sistema

Una vez iniciados los servicios locales:

- **Sistema de Inventario (Python / Flask):** [http://localhost:5000](http://localhost:5000)
- **Web Service de Contabilidad (C# / ASP.NET Core):** [http://localhost:5050](http://localhost:5050)
- **Credenciales por defecto:**
  - **Usuario:** `admin`
  - **Contraseña:** `admin123`
  - **Rol:** Encargado de Insumos

---

## Arquitectura y Tecnologías Empleadas

El proyecto está diseñado bajo una arquitectura de microservicios e interoperabilidad vía HTTP / REST:

### 1. Sistema de Inventario y Gestión Web (Python / Flask)
* **Tecnología:** Python 3 + Flask + SQLite 3 + Bootstrap 5 + Vanilla JavaScript.
* **Responsabilidad:**
  - Proporciona la interfaz gráfica de usuario completa (panel responsivo con Bootstrap 5).
  - Control de autenticación y sesiones para el Encargado de Insumos.
  - Gestión CRUD completa de Artículos, Almacenes y Tipos de Inventario con integridad referencial.
  - Registro de transacciones de inventario (Entradas, Salidas y Ajustes) con validación estricta de stock disponible.
  - Desglose de existencias por almacén en tiempo real.
  - **Cliente Web Service:** Al confirmar cada movimiento de inventario, genera y transmite de forma asíncrona/HTTP el correspondiente asiento contable hacia el microservicio en C#/.NET.

### 2. Web Service de Contabilidad Propietaria (C# / .NET 11)
* **Tecnología:** C# + ASP.NET Core Web API (.NET 11).
* **Responsabilidad:**
  - Funciona como un servicio de backend independiente que escucha en el puerto `5050`.
  - Expone una API REST para la recepción, validación y almacenamiento de **Asientos Contables** (`/api/contabilidad/asientos`).
  - Procesa débitos y créditos con cuentas contables según el tipo de movimiento de inventario (Cuentas de inventario, Cuentas por pagar, Costo de ventas).
  - Proporciona un endpoint de consulta para auditar todos los asientos contables procesados.

---

## Módulos del Sistema

### 1. Autenticación y Seguridad
- Acceso restringido para el Encargado de Insumos con contraseñas encriptadas mediante hashing (`werkzeug.security`).
- Decorador `@login_required` para protección de rutas y control de sesión.

### 2. Panel de Control (Dashboard)
- Indicadores cuantitativos del inventario: total de artículos, almacenes, tipos y transacciones.
- Visualización de los últimos movimientos realizados.

### 3. Gestión de Artículos
- CRUD completo con asignación de almacén de pertenencia, tipo de inventario y costo unitario.
- Ordenación dinámica por ID (ascendente/descendente).
- Vista detallada (icono de ojo) con desglose de existencias por cada almacén y su historial de movimientos.

### 4. Gestión de Almacenes
- Administración de depósitos físicos con validación de integridad referencial antes de eliminar.

### 5. Gestión de Tipos de Inventario
- Catálogo contable con cuentas asociadas para cada tipo de insumo (materia prima, productos terminados, etc.).

### 6. Gestión de Transacciones
- Registro de Entradas (ingreso a inventario), Salidas (validación de stock) y Ajustes.
- Cálculo automático de montos según cantidad y costo unitario.
- Emisión automática del asiento contable al Web Service C#/.NET.

### 7. Asientos Contables (Integración C# / .NET)
- Módulo visual en Flask que consulta en tiempo real al Web Service en C# (puerto 5050) para auditar los asientos generados por las transacciones.

---

## Instrucciones de Ejecución

### Prerrequisitos
- Python 3.10+ instalado y agregado al PATH.
- .NET SDK (versión 8.0, 9.0 o posterior).

### Pasos

1. **Iniciar el Web Service de Contabilidad (C# / .NET):**
   ```bash
   cd ContabilidadService
   dotnet run
   ```
   *(El servicio comenzará a escuchar en `http://localhost:5050`)*

2. **Iniciar el Sistema de Inventario (Python / Flask):**
   En una terminal separada:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
   *(La aplicación web estará disponible en `http://localhost:5000`)*

3. **Acceder:** Inicie sesión con el usuario `admin` y clave `admin123`.
