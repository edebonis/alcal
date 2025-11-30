import os
import re

BASE_DIR = '/home/esteban/Documentos/alcal/administracion/templates/administracion'

def limpiar_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Contenedor principal
    if '{% block content %}' in content and 'container-fluid' not in content:
        content = content.replace('{% block content %}', '{% block content %}\n<div class="container-fluid alcal-fade-in-up">')
        content = content.replace('{% endblock %}', '</div>\n{% endblock %}')

    # 2. Títulos y botones de cabecera
    # Buscar patrón: <div style="display: flex..."><h2...>...</h2><a...>...</a></div>
    # Reemplazar por estructura Bootstrap
    
    # Reemplazo genérico de estilos inline feos en títulos
    content = re.sub(r'<h2 style="[^"]*">', '<h1 class="h3 mb-0 text-gray-800">', content)
    content = content.replace('</h2>', '</h1>')
    
    # 3. Tablas
    if '<table>' in content:
        content = content.replace('<div class="table-container">', '<div class="card shadow border-0 mb-4"><div class="card-body"><div class="table-responsive">')
        content = content.replace('<table>', '<table class="table table-hover align-middle" width="100%" cellspacing="0">')
        content = content.replace('</table>', '</table></div></div></div>')
        # Eliminar cierre de table-container si existe
        content = content.replace('</div>\n{% else %}', '</div>\n{% else %}') # Hacky, mejor asumir estructura
    
    # 4. Thead
    content = content.replace('<thead>', '<thead class="bg-light small text-uppercase text-muted">')
    
    # 5. Botones
    content = content.replace('class="btn btn-alcal-primary"', 'class="btn btn-alcal-primary shadow-sm"')
    content = content.replace('class="btn btn-secondary"', 'class="btn btn-sm btn-outline-secondary"')
    content = content.replace('class="btn btn-danger"', 'class="btn btn-sm btn-outline-danger"')
    
    # 6. Eliminar estilos inline comunes
    content = re.sub(r'style="padding: [^"]*"', '', content)
    content = re.sub(r'style="font-size: [^"]*"', '', content)
    content = re.sub(r'style="margin-top: [^"]*"', '', content)
    
    # 7. Search bar
    if '<div class="search-bar">' in content:
        content = content.replace('<div class="search-bar">', '<div class="card shadow border-0 mb-4"><div class="card-body">')
        content = content.replace('<form method="get" style="display: flex; gap: 10px; width: 100%;">', '<form method="get" class="row g-3 align-items-center">')
        content = content.replace('<input type="text" name="q"', '<div class="col-md-4"><input type="text" name="q"')
        content = content.replace('value="{{ search }}">', 'value="{{ search }}"></div>')
        # Esto es muy frágil, mejor reescribir manualmente los list.html más importantes si el script falla.
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✨ Limpiado: {filepath}")
    else:
        print(f"⏭️ Sin cambios: {filepath}")

def recorrer_y_limpiar():
    print(f"Iniciando limpieza en {BASE_DIR}")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('list.html'):
                limpiar_template(os.path.join(root, file))

if __name__ == '__main__':
    recorrer_y_limpiar()
