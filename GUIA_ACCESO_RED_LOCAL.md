# 🌐 Guía de Acceso desde Red Local - Sistema ALCAL

## 📋 Resumen Rápido

Para acceder al sistema ALCAL desde cualquier dispositivo en tu red local, sigue estos pasos:

### 🚀 Método Rápido (Recomendado)

```bash
cd /home/esteban/Documentos/alcal
source venv/bin/activate
python start_server.py
```

El script automáticamente:
- ✅ Detecta tu IP local
- ✅ Encuentra un puerto disponible (8008 por defecto)
- ✅ Muestra las URLs de acceso

---

## 🔧 Opciones de Ejecución

### Opción 1: Script Automático (Recomendado)

```bash
cd /home/esteban/Documentos/alcal
source venv/bin/activate
python start_server.py
```

**Ventajas:**
- Detecta automáticamente tu IP local
- Busca puertos disponibles si el predeterminado está ocupado
- Muestra todas las URLs de acceso

**Salida esperada:**
```
🚀 Iniciando servidor ALCAL...
📍 IP Local: 192.168.68.111
🔌 Puerto: 8008
🌐 Acceso local: http://localhost:8008/admin/
📱 Acceso red: http://192.168.68.111:8008/admin/
```

---

### Opción 2: Comando Manual de Django

```bash
cd /home/esteban/Documentos/alcal
source venv/bin/activate
python manage.py runserver 0.0.0.0:8008
```

**Nota:** `0.0.0.0` permite acceso desde cualquier IP de la red local.

---

### Opción 3: Especificar IP Manualmente

Si conoces tu IP local específica:

```bash
cd /home/esteban/Documentos/alcal
source venv/bin/activate
python manage.py runserver 192.168.68.111:8008
```

---

## 📱 Acceso desde Dispositivos en la Red

Una vez que el servidor esté corriendo, podrás acceder desde:

### Desde tu computadora (localhost)
```
http://localhost:8008/
http://localhost:8008/admin/
```

### Desde cualquier dispositivo en la misma red
```
http://192.168.68.111:8008/
http://192.168.68.111:8008/admin/
```

**Reemplaza `192.168.68.111` con tu IP local real** (el script la mostrará al iniciar).

---

## 🔍 Verificar tu IP Local

Si necesitas conocer tu IP local manualmente:

```bash
# Opción 1: Comando simple
hostname -I

# Opción 2: Más detallado
ip addr show | grep "inet " | grep -v 127.0.0.1

# Opción 3: En Linux
ifconfig | grep "inet "
```

---

## 🔒 Configuración de Seguridad

El sistema está configurado con:

- ✅ `ALLOWED_HOSTS = ['*']` - Permite acceso desde cualquier IP
- ✅ `DEBUG = True` - Modo desarrollo activado
- ✅ Servidor escuchando en `0.0.0.0` - Acepta conexiones de todas las interfaces

**⚠️ IMPORTANTE:** Esta configuración es solo para desarrollo. En producción, debes:
- Configurar `ALLOWED_HOSTS` con IPs específicas
- Desactivar `DEBUG`
- Usar un servidor web profesional (nginx + gunicorn)

---

## 🛠️ Solución de Problemas

### El puerto está ocupado

Si el puerto 8008 está en uso, el script `start_server.py` automáticamente probará con:
- 8080
- 8081
- 8082
- 8083
- 8084
- 8085

O puedes especificar otro puerto manualmente:

```bash
python manage.py runserver 0.0.0.0:9000
```

### No puedo acceder desde otro dispositivo

1. **Verifica el firewall:**
   ```bash
   # En Ubuntu/Debian
   sudo ufw allow 8008
   
   # O desactivar temporalmente (solo desarrollo)
   sudo ufw disable
   ```

2. **Verifica que estés en la misma red:**
   - Ambos dispositivos deben estar en la misma red WiFi/LAN
   - No funcionará si uno está en WiFi y otro en datos móviles

3. **Verifica la IP:**
   - Asegúrate de usar la IP correcta que muestra el script
   - La IP puede cambiar si te conectas a otra red

### Error "DisallowedHost"

Si ves este error, verifica que `ALLOWED_HOSTS` en `settings.py` incluya `'*'` o tu IP específica.

---

## 📊 URLs Importantes

Una vez que el servidor esté corriendo:

| Recurso | URL |
|---------|-----|
| **Página principal** | `http://TU_IP:8008/` |
| **Admin Django** | `http://TU_IP:8008/admin/` |
| **API REST** | `http://TU_IP:8008/api/` |

---

## 👤 Credenciales de Acceso

### Superusuario
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Usuarios Demo (si existen)
- `demo_admin` / `admin123`
- `demo_docente` / `docente123`
- `demo_alumno` / `alumno123`

---

## 🎯 Ejemplo Completo

```bash
# 1. Ir al directorio del proyecto
cd /home/esteban/Documentos/alcal

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Iniciar servidor
python start_server.py

# Salida esperada:
# 🚀 Iniciando servidor ALCAL...
# 📍 IP Local: 192.168.68.111
# 🔌 Puerto: 8008
# 🌐 Acceso local: http://localhost:8008/admin/
# 📱 Acceso red: http://192.168.68.111:8008/admin/
# ==================================================
# 
# Starting development server at http://0.0.0.0:8008/
# Quit the server with CONTROL-C.
```

Luego, desde cualquier dispositivo en tu red, abre:
```
http://192.168.68.111:8008/admin/
```

---

## 📝 Notas Adicionales

- El servidor se detiene con `Ctrl+C`
- Si cambias de red WiFi, tu IP local cambiará
- Para acceso permanente, considera configurar una IP estática en tu router
- En producción, usa `gunicorn` o `uwsgi` con `nginx`

---

**Última actualización:** 2025-01-XX  
**Sistema ALCAL - Sagrado Corazón ALCAL**


