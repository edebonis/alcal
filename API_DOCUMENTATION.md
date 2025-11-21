# 📡 ALCAL API - Documentación REST API

## 🎯 Introducción

La API REST de ALCAL permite integrar el sistema de gestión académica con aplicaciones externas, móviles o servicios de terceros.

## 🔗 URLs Principales

- **Swagger UI**: `http://127.0.0.1:8008/api/v1/docs/`
- **ReDoc**: `http://127.0.0.1:8008/api/v1/redoc/`
- **Schema JSON**: `http://127.0.0.1:8008/api/v1/schema/`

## 🔐 Autenticación

La API utiliza **Session Authentication** de Django. Para acceder a los endpoints:

### Opción 1: Autenticación en Swagger UI
1. Navegar a `/api/v1/docs/`
2. Hacer clic en el botón **"Authorize"** (candado verde, arriba a la derecha)
3. Ingresar: usuario `edebonis` / contraseña `admin123`
4. Hacer clic en "Authorize"

### Opción 2: Programática (Example con Python)
```python
import requests

# Login
session = requests.Session()
login_url = 'http://127.0.0.1:8008/admin/login/'
response = session.post(login_url, data={
    'username': 'edebonis',
    'password': 'admin123'
})

# Usar la sesión para hacer requests
alumnos = session.get('http://127.0.0.1:8008/api/v1/alumnos/')
print(alumnos.json())
```

### Opción 3: cURL
```bash
# Login y guardar cookies
curl -c cookies.txt -d "username=edebonis&password=admin123" \
  http://127.0.0.1:8008/admin/login/

# Usar cookies para hacer requests
curl -b cookies.txt http://127.0.0.1:8008/api/v1/alumnos/
```

## 📊 Endpoints Disponibles

### 👥 Alumnos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/alumnos/` | Listar todos los alumnos |
| GET | `/api/v1/alumnos/{legajo}/` | Obtener detalle de un alumno |
| POST | `/api/v1/alumnos/` | Crear un nuevo alumno |
| PUT/PATCH | `/api/v1/alumnos/{legajo}/` | Actualizar un alumno |
| DELETE | `/api/v1/alumnos/{legajo}/` | Eliminar un alumno |
| GET | `/api/v1/alumnos/por_curso/?curso_id=1` | Filtrar alumnos por curso |

**Filtros disponibles**:
- `?curso=1` - Filtrar por curso
- `?activo=true` - Solo alumnos activos
- `?search=Juan` - Buscar por nombre/apellido/DNI

**Ejemplo de respuesta**:
```json
{
  "count": 130,
  "next": "http://127.0.0.1:8008/api/v1/alumnos/?page=2",
  "previous": null,
  "results": [
    {
      "legajo": 1,
      "nombre": "Diego",
      "apellido": "Vargas",
      "dni": 12345678,
      "curso": 1,
      "curso_nombre": "1A",
      "activo": true
    }
  ]
}
```

### 🏫 Escuela

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/carreras/` | Listar carreras |
| GET | `/api/v1/anios/` | Listar años lectivos |
| GET | `/api/v1/cursos/` | Listar cursos |
| GET | `/api/v1/materias/` | Listar materias |

### 📅 Asistencias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/asistencias/` | Listar asistencias |
| GET | `/api/v1/asistencias/{id}/` | Detalle de asistencia |
| POST | `/api/v1/asistencias/` | Registrar asistencia |
| GET | `/api/v1/asistencias/estadisticas/` | Estadísticas de asistencia |
| GET | `/api/v1/codigos-asistencia/` | Códigos disponibles (P, A, T, etc.) |
| GET | `/api/v1/turnos/` | Turnos disponibles |
| GET | `/api/v1/cierres-diarios/` | Historial de cierres |
| GET | `/api/v1/resumenes-diarios/` | Resúmenes por alumno |

**Filtros de asistencias**:
- `?curso=1`
- `?alumno=5`
- `?fecha=2025-11-20`
- `?fecha_desde=2025-11-01&fecha_hasta=2025-11-30`
- `?turno=1`
- `?procesado=true`

**Ejemplo - Crear asistencia**:
```json
POST /api/v1/asistencias/
{
  "ciclo_lectivo": 1,
  "curso": 1,
  "alumno": 5,
  "codigo": 1,
  "turno": 1,
  "fecha": "2025-11-21",
  "observaciones": "Llegó tarde por lluvia"
}
```

**Ejemplo - Estadísticas**:
```bash
GET /api/v1/asistencias/estadisticas/?curso=1&fecha=2025-11-21
```

Respuesta:
```json
{
  "total": 25,
  "por_codigo": [
    {"codigo__codigo": "P", "codigo__descripcion": "Presente", "cantidad": 20},
    {"codigo__codigo": "T", "codigo__descripcion": "Tarde (más de 15 min)", "cantidad": 3},
    {"codigo__codigo": "A", "codigo__descripcion": "Ausente", "cantidad": 2}
  ]
}
```

## 🔍 Paginación

Todos los endpoints de listado soportan paginación:

```bash
GET /api/v1/alumnos/?page=2&page_size=10
```

Respuesta incluye:
- `count`: Total de resultados
- `next`: URL de la siguiente página
- `previous`: URL de la página anterior
- `results`: Array de resultados

## 📖 Ordenamiento

Usa el parámetro `ordering`:

```bash
GET /api/v1/alumnos/?ordering=apellido
GET /api/v1/alumnos/?ordering=-apellido  # DESC
GET /api/v1/asistencias/?ordering=-fecha,alumno__apellido
```

## 🎨 Formato de Respuesta

Por defecto, la API devuelve JSON. Para otros formatos:

```bash
GET /api/v1/alumnos/?format=json
GET /api/v1/alumnos/?format=api  # Browsable API
```

## ⚠️ Manejo de Errores

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**Solución**: Autenticarse primero.

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```
**Solución**: El usuario no tiene permisos para esta acción.

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "curso": ["This field is required."],
  "fecha": ["Enter a valid date."]
}
```

## 🚀 Ejemplos de Uso

### Obtener alumnos de un curso específico
```python
import requests

session = requests.Session()
# ... autenticar ...

alumnos = session.get('http://127.0.0.1:8008/api/v1/alumnos/', params={
    'curso': 1,
    'activo': True,
    'ordering': 'apellido'
}).json()

for alumno in alumnos['results']:
    print(f"{alumno['apellido']}, {alumno['nombre']}")
```

### Registrar asistencias del día
```python
from datetime import date

asistencias = [
    {'alumno': 1, 'codigo': 1},  # Presente
    {'alumno': 2, 'codigo': 3},  # Tarde
    {'alumno': 3, 'codigo': 4},  # Ausente
]

for asis in asistencias:
    session.post('http://127.0.0.1:8008/api/v1/asistencias/', json={
        'ciclo_lectivo': 1,
        'curso': 1,
        'alumno': asis['alumno'],
        'codigo': asis['codigo'],
        'turno': 1,
        'fecha': str(date.today())
    })
```

### Consultar resumen de faltas de un alumno
```python
resumenes = session.get('http://127.0.0.1:8008/api/v1/resumenes-diarios/', params={
    'alumno': 5,
    'fecha_desde': '2025-11-01',
    'fecha_hasta': '2025-11-30'
}).json()

total_faltas = sum(r['valor_falta_final'] for r in resumenes['results'])
print(f"Total de faltas: {total_faltas}")
```

## 🔧 Configuración Avanzada

### CORS (para frontend externo)

Ya está configurado en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

Agrega tu dominio si es necesario.

### Permisos Personalizados

Los endpoints usan `IsAuthenticated` por defecto. Para cambiar permisos específicos, edita el ViewSet:

```python
# asistencias/viewsets.py
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AsistenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Cambiar según necesites
```

## 📚 Recursos Adicionales

- **Documentación DRF**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/

---

**Versión**: 1.0.0  
**Última actualización**: 2025-11-21
