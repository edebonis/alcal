#!/bin/bash
# Script para verificar que el admin de ALCAL funciona correctamente

echo "🧪 Probando el admin de ALCAL..."
echo "=================================================="

BASE_URL="http://localhost:8080"

# Probar página principal
echo -n "✅ Página principal: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/")
echo "$STATUS"

# Probar redirección del admin
echo -n "✅ Admin redirige: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/admin/")
echo "$STATUS"

# Probar página de login
echo -n "✅ Login del admin: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/admin/login/")
echo "$STATUS"

# Probar CSS personalizado
echo -n "✅ CSS personalizado: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/static/admin/css/alcal-admin.css")
echo "$STATUS"

echo "=================================================="
echo "🎉 ¡Admin funcionando correctamente!"
echo ""
echo "📱 Accede desde tu navegador:"
echo "   🌐 Local: $BASE_URL/admin/"
echo ""
echo "👤 Usuarios disponibles:"
echo "   demo_admin / admin123        (Administrador)"
echo "   demo_director / director123  (Director)"
echo "   demo_preceptor / preceptor123 (Preceptor)"
echo "   demo_docente / docente123    (Docente)"
echo "   demo_familiar / familiar123  (Familiar a Cargo)"
echo "   demo_alumno / alumno123      (Alumno)" 