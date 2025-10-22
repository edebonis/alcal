#!/usr/bin/env python3
"""
Script para verificar que el admin de ALCAL funciona correctamente
"""
import sys

import requests


def test_admin():
    base_url = "http://localhost:8080"
    
    print("🧪 Probando el admin de ALCAL...")
    print("=" * 50)
    
    # Probar página principal
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Página principal: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en página principal: {e}")
        return False
    
    # Probar redirección del admin
    try:
        response = requests.get(f"{base_url}/admin/", allow_redirects=False)
        if response.status_code == 302:
            print(f"✅ Admin redirige correctamente: {response.status_code}")
        else:
            print(f"⚠️  Admin respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en admin: {e}")
        return False
    
    # Probar página de login
    try:
        response = requests.get(f"{base_url}/admin/login/")
        if response.status_code == 200 and "csrfmiddlewaretoken" in response.text:
            print(f"✅ Login del admin: {response.status_code} (con CSRF)")
        else:
            print(f"❌ Login del admin: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
    
    # Probar archivos estáticos
    try:
        response = requests.get(f"{base_url}/static/admin/css/alcal-admin.css")
        if response.status_code == 200:
            print(f"✅ CSS personalizado: {response.status_code}")
        else:
            print(f"⚠️  CSS personalizado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en CSS: {e}")
    
    print("=" * 50)
    print("🎉 ¡Admin funcionando correctamente!")
    print()
    print("📱 Accede desde tu navegador:")
    print(f"   🌐 Local: {base_url}/admin/")
    print()
    print("👤 Usuarios disponibles:")
    print("   demo_admin / admin123        (Administrador)")
    print("   demo_director / director123  (Director)")
    print("   demo_preceptor / preceptor123 (Preceptor)")
    print("   demo_docente / docente123    (Docente)")
    print("   demo_familiar / familiar123  (Familiar a Cargo)")
    print("   demo_alumno / alumno123      (Alumno)")
    
    return True

if __name__ == "__main__":
    if test_admin():
        sys.exit(0)
    else:
        sys.exit(1) 