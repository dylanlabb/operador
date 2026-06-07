"""
Genera _site/ con HTML estático para GitHub Pages o Netlify.
Uso: python build.py
"""
import os, re, shutil
from app import app

BASE   = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, '_site')

PAGES = [
    ('/',                             'index.html'),
    ('/nosotros',                     'nosotros/index.html'),
    ('/servicios',                    'servicios/index.html'),
    ('/productos',                    'productos/index.html'),
    ('/productos?categoria=tanques',  'productos/tanques/index.html'),
    ('/productos?categoria=plastico', 'productos/plastico/index.html'),
    ('/productos?categoria=metal',    'productos/metal/index.html'),
    ('/productos?categoria=bidones',  'productos/bidones/index.html'),
    ('/contacto',                     'contacto/index.html'),
]

PAGES_MAP = ['nosotros', 'servicios', 'productos', 'contacto']

def make_relative(html, depth):
    up = '../' * depth

    html = re.sub(r'(href|src)="/static/', lambda m: f'{m.group(1)}="{up}static/', html)
    html = html.replace('action="/contacto"', f'action="{up}contacto/"')

    for page in PAGES_MAP:
        html = re.sub(f'href="/{page}"',  f'href="{up}{page}/"', html)
        html = re.sub(f'href="/{page}/',  f'href="{up}{page}/', html)

    html = re.sub(r'href="/"', f'href="{up}index.html"', html)

    html = re.sub(
        r'href="(?:\.\.\/)*productos\?categoria=(\w+)"',
        lambda m: f'href="{up}productos/{m.group(1)}/"',
        html
    )

    return html

def fix_contact_form(html):
    html = html.replace(
        'method="POST" action="',
        'method="POST" data-netlify="true" name="contacto" action="'
    )
    html = re.sub(
        r'(<form[^>]+data-netlify="true"[^>]*>)',
        r'\1\n    <input type="hidden" name="form-name" value="contacto">',
        html
    )
    return html

if os.path.exists(OUTPUT):
    shutil.rmtree(OUTPUT)
os.makedirs(OUTPUT)

with app.test_client() as client:
    for route, out_file in PAGES:
        html  = client.get(route).data.decode('utf-8')
        depth = out_file.count('/')
        html  = make_relative(html, depth)
        html  = fix_contact_form(html)

        dest = os.path.join(OUTPUT, out_file)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  OK  {out_file}')

shutil.copytree(os.path.join(BASE, 'static'), os.path.join(OUTPUT, 'static'))
print('  OK  static/')
print('\nListo.')
