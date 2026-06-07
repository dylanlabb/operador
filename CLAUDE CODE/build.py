"""
Genera la carpeta _site/ con HTML estático para subir a Netlify.
Uso: .venv\Scripts\python.exe build.py
"""
import os, re, shutil
from app import app

BASE   = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, '_site')

# Páginas a generar: (ruta Flask, archivo de salida)
PAGES = [
    ('/',                          'index.html'),
    ('/nosotros',                  'nosotros/index.html'),
    ('/servicios',                 'servicios/index.html'),
    ('/productos',                 'productos/index.html'),
    ('/productos?categoria=tanques',  'productos/tanques/index.html'),
    ('/productos?categoria=plastico', 'productos/plastico/index.html'),
    ('/productos?categoria=metal',    'productos/metal/index.html'),
    ('/productos?categoria=bidones',  'productos/bidones/index.html'),
    ('/contacto',                  'contacto/index.html'),
]

def fix_html(html, route):
    # Filtros productos: ?categoria=X → /productos/X
    html = re.sub(
        r'href="/productos\?categoria=(\w+)"',
        r'href="/productos/\1"',
        html
    )
    # Formulario de contacto: añadir soporte Netlify Forms
    html = html.replace(
        'method="POST" action="/contacto"',
        'method="POST" action="/contacto" data-netlify="true" name="contacto"'
    )
    html = re.sub(
        r'(<form[^>]+data-netlify="true"[^>]*>)',
        r'\1\n    <input type="hidden" name="form-name" value="contacto">',
        html
    )
    return html

# Limpiar salida anterior
if os.path.exists(OUTPUT):
    shutil.rmtree(OUTPUT)
os.makedirs(OUTPUT)

with app.test_client() as client:
    for route, out_file in PAGES:
        html = client.get(route).data.decode('utf-8')
        html = fix_html(html, route)
        dest = os.path.join(OUTPUT, out_file)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  OK  {out_file}')

# Copiar archivos estáticos
shutil.copytree(os.path.join(BASE, 'static'), os.path.join(OUTPUT, 'static'))
print('  OK  static/')

# _redirects para Netlify (rutas sin .html)
with open(os.path.join(OUTPUT, '_redirects'), 'w') as f:
    f.write('/contacto  /contacto/index.html  200\n')

print(f'\nListo. Sube la carpeta  _site/  a Netlify.')
