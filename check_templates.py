#!/usr/bin/env python3
"""Lint all Django templates for syntax errors.
Run with:
    python check_templates.py
"""
import os
import sys
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')

import django
django.setup()  # Initialise Django apps before loading templates

from django.template import loader, TemplateDoesNotExist, TemplateSyntaxError

def main():
    # Directories that contain our project templates (ignore third‑party packages)
    template_dirs = [
        PROJECT_ROOT / 'templates',
        PROJECT_ROOT / 'administracion' / 'templates',
        PROJECT_ROOT / 'asistencias' / 'templates',
    ]

    errors = []
    for base in template_dirs:
        for path in base.rglob('*.html'):
            rel_path = path.relative_to(PROJECT_ROOT)
            template_name = str(rel_path).replace(os.sep, '/')
            try:
                loader.get_template(template_name)
            except TemplateSyntaxError as e:
                errors.append((template_name, str(e)))
            except TemplateDoesNotExist:
                # Should not happen for our own templates, ignore silently
                pass
            except Exception as e:
                errors.append((template_name, f'Unexpected error: {e}'))

    if errors:
        print('Template syntax errors found:')
        for tmpl, msg in errors:
            print(f' - {tmpl}: {msg}')
        sys.exit(1)
    else:
        print('All project templates compiled successfully.')
        sys.exit(0)

if __name__ == '__main__':
    main()
