import os
import re

BASE_DIR = '/home/esteban/Documentos/alcal/administracion/templates/administracion'

def migrar_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Cambiar extends
    if "{% extends 'administracion/base.html' %}" in content:
        content = content.replace("{% extends 'administracion/base.html' %}", "{% extends 'base_modern.html' %}")
        
        # 2. Ajustar bloques si es necesario
        # base_modern usa 'content', administracion/base usa 'content' también. Compatible.
        
        # 3. Ajustar clases de botones para estilo premium
        content = content.replace('btn-primary', 'btn-alcal-primary')
        content = content.replace('text-primary', 'text-alcal-primary')
        content = content.replace('bg-primary', 'bg-alcal-primary')
        
        # 4. Ajustar contenedores
        # Si tiene container-fluid, agregar clase de animación
        content = content.replace('class="container-fluid"', 'class="container-fluid alcal-fade-in-up"')
        
        # 5. Ajustar tarjetas
        content = content.replace('card shadow mb-4', 'card shadow border-0 mb-4')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Migrado: {filepath}")
    else:
        print(f"⏭️ Saltado (ya migrado o diferente): {filepath}")

def recorrer_y_migrar():
    print(f"Iniciando migración en {BASE_DIR}")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.html'):
                migrar_template(os.path.join(root, file))

if __name__ == '__main__':
    recorrer_y_migrar()
