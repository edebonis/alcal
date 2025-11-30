import os

BASE_DIR = '/home/esteban/Documentos/alcal/administracion/templates/administracion'

def corregir_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corregir error en block title
    # Busca {% block title %}Titulo</div>{% endblock %}
    # Reemplaza por {% block title %}Titulo{% endblock %}
    
    new_content = content.replace('</div>\n{% endblock %}\n\n{% block content %}', '{% endblock %}\n\n{% block content %}')
    # Si el title y content están separados de otra forma
    import re
    new_content = re.sub(r'({% block title %}.*?)</div>(\s*{% endblock %})', r'\1\2', new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"🔧 Corregido: {filepath}")
    else:
        print(f"👌 OK: {filepath}")

def recorrer_y_corregir():
    print(f"Iniciando corrección en {BASE_DIR}")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('list.html'):
                corregir_template(os.path.join(root, file))

if __name__ == '__main__':
    recorrer_y_corregir()
