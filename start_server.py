#!/usr/bin/env python
"""
Script personalizado para iniciar el servidor Django ALCAL
Optimizado para macOS y acceso desde red local
"""
import os
import socket
import subprocess
import sys
from pathlib import Path


def get_local_ip():
    """Obtiene la IP local de la máquina"""
    try:
        # Conecta a un servidor externo para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "192.168.68.13"  # IP conocida como fallback

def check_port_available(port):
    """Verifica si un puerto está disponible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', port))
        sock.close()
        return True
    except OSError:
        return False

def main():
    # Configurar el entorno Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
    
    # Obtener IP local
    local_ip = get_local_ip()
    port = 8080
    
    # Verificar si el puerto está disponible
    if not check_port_available(port):
        print(f"❌ Puerto {port} no está disponible")
        # Intentar con otros puertos
        for test_port in [8081, 8082, 8083, 8084, 8085]:
            if check_port_available(test_port):
                port = test_port
                break
        else:
            print("❌ No se encontró un puerto disponible")
            sys.exit(1)
    
    print("🚀 Iniciando servidor ALCAL...")
    print(f"📍 IP Local: {local_ip}")
    print(f"🔌 Puerto: {port}")
    print(f"🌐 Acceso local: http://localhost:{port}/admin/")
    print(f"📱 Acceso red: http://{local_ip}:{port}/admin/")
    print("=" * 50)
    print("👤 Usuarios demo disponibles:")
    print("   demo_admin / admin123")
    print("   demo_director / director123")
    print("   demo_preceptor / preceptor123")
    print("   demo_docente / docente123")
    print("   demo_familiar / familiar123")
    print("   demo_alumno / alumno123")
    print("=" * 50)
    
    # Iniciar el servidor Django
    try:
        cmd = [
            sys.executable, 
            'manage.py', 
            'runserver', 
            f'0.0.0.0:{port}',
            '--noreload'  # Evita problemas con el reloader en macOS
        ]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")

if __name__ == '__main__':
    main() 