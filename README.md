# Sistema Integral de Gestión de Inventario con Integración Contable Automatizada (ISO815)

Proyecto final desarrollado para la asignatura **ISO815** y aplicable a la asignatura de **Tecnología Propietaria**. El sistema implementa una arquitectura orientada a servicios que sitúa la gestión de inventario como núcleo operativo principal, complementada por un microservicio independiente desarrollado en **C# / ASP.NET Core** que procesa de manera automática el impacto contable derivado de cada movimiento de inventario.

---

## 1. Concepto General del Sistema

El proyecto tiene como propósito principal brindar un control integral, confiable y trazable de las existencias, almacenes, artículos y movimientos de insumos en una organización. 

Para respaldar la gestión operativa sin transformarse en un sistema de contabilidad general o ERP independiente, el sistema incorpora un servicio complementario en C#/.NET que recibe notificaciones de cada transacción de inventario (entradas, salidas y ajustes), determina las cuentas contables aplicables (débito y crédito) y almacena el registro del impacto contable garantizando la trazabilidad entre el movimiento físico y su reflejo financiero.

---

## 2. Arquitectura Tecnológica

La solución se estructura en tres componentes tecnológicos bien delimitados que interactúan mediante protocolos estándar HTTP / REST:

### 1. Sistema Principal de Gestión de Inventario – Python + Flask
* **Tecnología:** Python 3 + Flask + Bootstrap 5 + Vanilla JavaScript.
* **Responsabilidad:**
  - Control de acceso y autenticación con contraseñas encriptadas para el encargado de insumos.
  - Gestión integral (CRUD) de Artículos, Almacenes y Tipos de Inventario con integridad referencial.
  - Registro y validación estricta de transacciones de inventario (Entradas, Salidas con control de existencias, y Ajustes).
  - Consulta de existencias globales y desglosadas por almacén físico.
  - Notificación automática mediante cliente HTTP/REST al servicio complementario ante cada movimiento registrado.

### 2. Servicio Complementario de Integración Contable – C# + ASP.NET Core
* **Tecnología:** C# + ASP.NET Core Web API (.NET 11).
* **Responsabilidad:**
  - Servicio complementario que escucha en el puerto `5050`.
  - Recibe notificaciones de movimientos originados exclusivamente en el sistema de inventario.
  - Asigna las cuentas de débito y crédito correspondientes según el tipo de operación y categoría del insumo.
  - Genera y resguarda los registros de impacto contable con identificación de trazabilidad (`TransaccionId`).
  - Previene registros duplicados en caso de reintentos de envío de una misma transacción.
  - Expone endpoints de auditoría y métricas para monitorear el estado del servicio y el volumen de operaciones procesadas.

### 3. Almacenamiento de Información – SQLite
* **Tecnología:** SQLite 3 relacional con foreign keys habilitadas.
* **Responsabilidad:**
  - Almacenamiento persistente y centralizado de los datos del sistema principal (usuarios, artículos, almacenes, tipos de inventario y transacciones).
  - Mantenimiento de la integridad referencial y soporte de transacciones ACID.

---

## 3. Módulos del Sistema de Inventario

1. **Autenticación y Sesiones:** Acceso restringido para el encargado de insumos mediante credenciales seguras con hash (`werkzeug.security`).
2. **Tablero Principal (Dashboard):** Visualización consolidada de métricas de inventario (total de artículos, almacenes, tipos, movimientos registrados y accesos directos).
3. **Catálogo de Artículos:** Alta, baja, modificación y consulta detallada de insumos, incluyendo existencias por almacén y ordenamiento dinámico por identificador (ascendente y descendente).
4. **Administración de Almacenes:** Gestión de ubicaciones físicas de almacenamiento con verificación de integridad previa a la eliminación.
5. **Tipos de Inventario:** Clasificación técnica de insumos con asignación de cuentas contables para su posterior integración.
6. **Transacciones de Inventario:** Registro de entradas, salidas y ajustes de stock con cálculo automático de importes y validación de existencias.
7. **Integración Contable:** Pantalla de supervisión que expone el estado de conexión del microservicio C#, resumen de operaciones (contabilizadas, pendientes y errores) y la tabla de trazabilidad contable ligada a cada movimiento de inventario.

---

## 4. Parámetros de Acceso Local

Una vez iniciados los servicios:

* **Sistema de Inventario (Python / Flask):** [http://localhost:5000](http://localhost:5000)
* **Servicio de Integración Contable (C# / ASP.NET Core):** [http://localhost:5050](http://localhost:5050)
* **Credenciales de Acceso:**
  * **Usuario:** `admin`
  * **Contraseña:** `admin123`
  * **Rol:** Encargado de Insumos

---

## 5. Instrucciones de Ejecución

### Prerrequisitos
* Python 3.10 o superior configurado en el sistema.
* .NET SDK (8.0, 9.0 o posterior).

### Pasos de Inicio

1. **Iniciar el Servicio de Integración Contable (C# / .NET):**
   ```bash
   cd ContabilidadService
   dotnet run
   ```
   *(El microservicio quedará activo en `http://localhost:5050`)*

2. **Iniciar el Sistema Principal de Inventario (Python / Flask):**
   En una terminal independiente dentro de la raíz del proyecto:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
   *(La aplicación principal estará disponible en `http://localhost:5000`)*

3. **Ingreso:** Abra su navegador en `http://localhost:5000` e ingrese con las credenciales indicadas.
