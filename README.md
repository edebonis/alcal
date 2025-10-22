# ALCAL - Sistema de Gestión Académica

Sistema integral de gestión para instituciones educativas desarrollado en Django.

## 🚀 Características

- **👥 Gestión de Alumnos**: Registro completo con datos familiares
- **👨‍🏫 Gestión de Docentes**: Control de profesores y materias
- **🏫 Estructura Académica**: Carreras, cursos, materias y ciclos lectivos
- **📊 Sistema de Calificaciones**: Notas trimestrales y parciales
- **📅 Control de Asistencias**: Sistema complejo de códigos de asistencia
- **📝 Observaciones**: Registro de incidentes y seguimiento estudiantil
- **🔐 API REST**: Endpoints para integración con aplicaciones externas

## 🛠️ Tecnologías

- **Backend**: Django 5.1.3
- **Base de Datos**: PostgreSQL
- **API**: Django REST Framework
- **Admin Interface**: Django Grappelli
- **Testing**: pytest + coverage

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd alcal
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements_new.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Configurar base de datos

```bash
# Crear base de datos PostgreSQL
createdb sag

# Ejecutar migraciones
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar tests con coverage
python -m pytest --cov=.

# Ejecutar tests específicos
python -m pytest tests/test_basic.py
```

## 📁 Estructura del Proyecto

```
alcal/
├── alcal/              # Configuración principal
├── alumnos/           # Gestión de alumnos
├── docentes/          # Gestión de docentes
├── escuela/           # Estructura académica
├── calificaciones/    # Sistema de notas
├── asistencias/       # Control de asistencias
├── observaciones/     # Registro de observaciones
├── templates/         # Plantillas HTML
├── tests/             # Tests del proyecto
└── requirements_new.txt
```

## 🔐 Configuración de Seguridad

### Variables de Entorno Requeridas

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
ALLOWED_HOSTS=your-domain.com,localhost
```

### Configuraciones de Producción

- Cambiar `DEBUG=False`
- Configurar `SECRET_KEY` única
- Configurar `ALLOWED_HOSTS` apropiadamente
- Usar HTTPS en producción
- Configurar respaldos de base de datos

## 📊 API Endpoints

### Autenticación

- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/logout/` - Cerrar sesión

### Recursos (Requieren autenticación)

- `GET /api/alumnos/` - Listar alumnos
- `GET /api/docentes/` - Listar docentes
- `GET /api/cursos/` - Listar cursos
- `GET /api/calificaciones/` - Listar calificaciones

## 🚀 Deployment

### Usando Heroku

1. Instalar Heroku CLI
2. Configurar variables de entorno
3. Deployar aplicación

```bash
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, crear un issue en GitHub.

## 📅 Roadmap

### Fase 1 - Estabilización ✅

- [x] Actualizar Django a 5.1
- [x] Configurar variables de entorno
- [x] Implementar tests básicos
- [x] Mejorar seguridad

### Fase 2 - Modernización (En Progreso)

- [ ] Crear API REST completa
- [ ] Implementar frontend moderno
- [ ] Dashboard interactivo
- [ ] Sistema de reportes

### Fase 3 - Funcionalidades Avanzadas

- [ ] App móvil
- [ ] Sistema de notificaciones
- [ ] Analytics predictivos
- [ ] Integración con sistemas externos
