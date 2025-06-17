#!/usr/bin/env python3
"""
Servidor proxy para ALCAL - Solución para acceso desde red local en macOS
Este script crea un proxy que redirige las conexiones de red al servidor Django local
"""
import os
import socket
import subprocess
import sys
import threading
import time


class ProxyServer:
    def __init__(self, local_host='127.0.0.1', local_port=8080, proxy_port=8081):
        self.local_host = local_host
        self.local_port = local_port
        self.proxy_port = proxy_port
        self.running = False
        
    def handle_client(self, client_socket):
        """Maneja una conexión de cliente"""
        try:
            # Conectar al servidor Django local
            django_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            django_socket.connect((self.local_host, self.local_port))
            
            # Función para reenviar datos
            def forward_data(source, destination):
                try:
                    while True:
                        data = source.recv(4096)
                        if not data:
                            break
                        destination.send(data)
                except:
                    pass
                finally:
                    source.close()
                    destination.close()
            
            # Crear hilos para reenviar datos en ambas direcciones
            client_to_django = threading.Thread(
                target=forward_data, 
                args=(client_socket, django_socket)
            )
            django_to_client = threading.Thread(
                target=forward_data, 
                args=(django_socket, client_socket)
            )
            
            client_to_django.daemon = True
            django_to_client.daemon = True
            
            client_to_django.start()
            django_to_client.start()
            
            # Esperar a que terminen los hilos
            client_to_django.join()
            django_to_client.join()
            
        except Exception as e:
            print(f"Error en proxy: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def start(self):
        """Inicia el servidor proxy"""
        self.running = True
        
        # Crear socket del proxy
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            proxy_socket.bind(('0.0.0.0', self.proxy_port))
            proxy_socket.listen(5)
            
            print(f"🔄 Proxy iniciado en puerto {self.proxy_port}")
            print(f"🎯 Redirigiendo a Django en {self.local_host}:{self.local_port}")
            
            while self.running:
                try:
                    client_socket, addr = proxy_socket.accept()
                    print(f"📱 Conexión desde: {addr}")
                    
                    # Manejar cliente en un hilo separado
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("Error en socket del proxy")
                    break
                    
        except Exception as e:
            print(f"❌ Error al iniciar proxy: {e}")
        finally:
            proxy_socket.close()
    
    def stop(self):
        """Detiene el servidor proxy"""
        self.running = False

def get_local_ip():
    """Obtiene la IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "192.168.68.13"

def main():
    local_ip = get_local_ip()
    django_port = 8080
    proxy_port = 8081
    
    print("🚀 Iniciando ALCAL con Proxy de Red")
    print("=" * 50)
    print(f"📍 IP Local: {local_ip}")
    print(f"🌐 Acceso local: http://localhost:{django_port}/admin/")
    print(f"📱 Acceso red: http://{local_ip}:{proxy_port}/admin/")
    print("=" * 50)
    print("👤 Usuarios demo:")
    print("   demo_admin / admin123")
    print("   demo_director / director123")
    print("   demo_preceptor / preceptor123")
    print("   demo_docente / docente123")
    print("   demo_familiar / familiar123")
    print("   demo_alumno / alumno123")
    print("=" * 50)
    
    # Verificar si Django está corriendo
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex(('127.0.0.1', django_port))
        test_socket.close()
        
        if result != 0:
            print(f"❌ Django no está corriendo en puerto {django_port}")
            print("   Ejecuta primero: python manage.py runserver 127.0.0.1:8080")
            return
        else:
            print(f"✅ Django detectado en puerto {django_port}")
    except:
        print("❌ Error al verificar Django")
        return
    
    # Iniciar proxy
    proxy = ProxyServer('127.0.0.1', django_port, proxy_port)
    
    try:
        proxy.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo proxy...")
        proxy.stop()

if __name__ == '__main__':
    main() 