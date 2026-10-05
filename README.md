# Sistema de Inventario para PYMEs - API REST Backend
**Evaluación N.° 2 - Backend**  
**Estudiante:** Jairo Contreras  
**Tecnologías:** Django 6.1, Django REST Framework 3.18, MySQL (XAMPP / MariaDB), Python 3.14

---

## 1. Descripción del Proyecto
Este proyecto implementa una API REST modular y escalable para la gestión de inventario de pequeñas y medianas empresas (PYMEs), cumpliendo con los estándares de diseño RESTful, persistencia desacoplada en MySQL y validaciones de reglas de negocio mediante serializadores de Django REST Framework (DRF).

---

## 2. Requisitos Previos
* **Python**: Versión 3.10 o superior (recomendado 3.11, 3.12, 3.13 o 3.14).
* **XAMPP**: Con el servicio **MySQL** activo en el puerto `3306`.
* **Git**: Para control de versiones.

---

## 3. Guía Rápida de Instalación y Puesta en Marcha

### Paso 1: Iniciar MySQL en XAMPP
1. Abre **XAMPP Control Panel**.
2. Haz clic en el botón **Start** al lado del módulo **MySQL** (debe quedar en verde en el puerto 3306).

### Paso 2: Crear la Base de Datos
Puedes crearla desde la consola o desde **phpMyAdmin** (`http://localhost/phpmyadmin`):
```sql
CREATE DATABASE IF NOT EXISTS pymes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
*(También se incluye el script completo en `scripts/01_init_db.sql`)*.

### Paso 3: Configurar el Entorno Virtual e Instalar Dependencias
Desde la raíz del proyecto en tu terminal (PowerShell o CMD):
```powershell
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual (PowerShell)
.\.venv\Scripts\Activate.ps1
# O en CMD tradicional:
# .\.venv\Scripts\activate.bat

# Instalar librerías
pip install -r requirements.txt
```

### Paso 4: Variables de Entorno (.env)
El archivo `.env` ya viene configurado para conectarse directamente a XAMPP:
```ini
SECRET_KEY=django-insecure-0r*^@7yq%+n1gaqs57+rcg_$ux(ls2uv_1!c1aryr-by+7b&(g
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.mysql
DB_NAME=pymes_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Paso 5: Aplicar Migraciones
Aplica las tablas a tu base de datos MySQL en XAMPP:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 6: (Opcional) Cargar Datos Iniciales o Crear Superusuario
```powershell
# Cargar datos de prueba
python manage.py loaddata pymesApp/fixtures/datos_iniciales.json

# Crear superusuario para el panel de administración
python manage.py createsuperuser
```

### Paso 7: Ejecutar el Servidor
```powershell
python manage.py runserver
```
Accede a:
* **API Navegable (DRF):** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
* **Panel de Administración:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **Página de Bienvenida:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 4. Documentación de Endpoints RESTful

| Recurso | Método HTTP | Endpoint | Acción | Descripción |
| :--- | :---: | :--- | :--- | :--- |
| **Categorías** | `GET` | `/api/categorias/` | Listar | Obtiene lista de categorías y total de productos asociados. |
| **Categorías** | `POST` | `/api/categorias/` | Crear | Registra una nueva categoría. |
| **Categoría** | `GET` | `/api/categorias/{id}/` | Detalle | Obtiene información detallada de una categoría. |
| **Categoría** | `PUT` | `/api/categorias/{id}/` | Actualizar | Reemplaza todos los datos de la categoría. |
| **Categoría** | `PATCH`| `/api/categorias/{id}/` | Parcial | Modifica atributos específicos de la categoría. |
| **Categoría** | `DELETE`| `/api/categorias/{id}/`| Eliminar | Borra la categoría si no posee productos vinculados (`PROTECT`). |
| **Productos** | `GET` | `/api/productos/` | Listar | Retorna lista de productos registrados. |
| **Productos** | `POST` | `/api/productos/` | Crear | Inserta producto. Valida `precio_estimado >= 0`. |
| **Producto** | `GET` | `/api/productos/{id}/` | Detalle | Detalle por clave primaria. |
| **Producto** | `PUT` | `/api/productos/{id}/` | Actualizar | Reemplazo completo del producto. |
| **Producto** | `PATCH`| `/api/productos/{id}/` | Parcial | Edición parcial (ej: actualizar únicamente stock). |
| **Producto** | `DELETE`| `/api/productos/{id}/`| Eliminar | Elimina el registro del producto. |

---

## 5. Ejemplos de Carga Útil (Payloads JSON)

### Crear Categoría (POST /api/categorias/)
```json
{
  "nombre": "Herramientas",
  "descripcion": "Herramientas de ferretería y construcción"
}
```

### Crear Producto (POST /api/productos/)
```json
{
  "nombre": "Taladro Percutor 750W",
  "descripcion": "Taladro profesional con velocidad variable",
  "precio_estimado": "45990.00",
  "stock": 20,
  "stock_minimo": 5,
  "disponible": true,
  "categoria": 1
}
```

### Regla de Validación de Negocio (`validate_precio_estimado`)
Si se envía un valor negativo como `"precio_estimado": -500`, la API rechaza la solicitud retornando código HTTP `400 Bad Request`:
```json
{
  "precio_estimado": [
    "El precio estimado no puede ser un valor negativo."
  ]
}
```
