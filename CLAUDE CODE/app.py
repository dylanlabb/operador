from urllib.parse import quote
from flask import Flask, render_template, request, flash, redirect, url_for, Response
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'orSAC-cambiar-en-produccion-2024'


@app.template_filter('urlencode')
def urlencode_filter(value: str) -> str:
    return quote(str(value), safe='')

PRODUCTOS = [
    {
        'id': 1,
        'nombre': 'Tanque MX de 275 galones',
        'descripcion': 'Contenedor de gran capacidad (275 galones / ~1040 litros) con estructura de acero galvanizado y base pallet. Ideal para almacenamiento y transporte de grandes volúmenes de líquidos industriales.',
        'usos': ['Aceites y lubricantes industriales', 'Productos químicos', 'Agua para procesos industriales', 'Solventes y soluciones industriales'],
        'categoria': 'tanques',
        'imagen': '/static/img/products/tanque-mx-275gal.jpg',
        'badge': 'Mayor demanda',
    },
    {
        'id': 2,
        'nombre': 'Cilindro con Tapa y Seguro Grande',
        'descripcion': 'Cilindro de polietileno de alta densidad (PEAD) de gran capacidad con sistema de tapa y seguro hermético. Resistente a impactos y a una amplia variedad de productos químicos.',
        'usos': ['Almacenamiento de solventes', 'Residuos líquidos industriales', 'Almacenamiento de agua industrial', 'Productos de limpieza'],
        'categoria': 'plastico',
        'imagen': '/static/img/products/cilindro-plastico-tapa-seguro.jpg',
        'badge': 'Mayor demanda',
    },
    {
        'id': 3,
        'nombre': 'Cilindro con Tapa Pequeña',
        'descripcion': 'Cilindro de polietileno de alta densidad (PEAD) con tapa de rosca pequeña. Ligero, manejable y resistente, apto para una amplia variedad de líquidos industriales.',
        'usos': ['Aceites lubricantes', 'Detergentes industriales', 'Productos de limpieza', 'Solventes'],
        'categoria': 'plastico',
        'imagen': '/static/img/products/cilindro-plastico-tapa-pequena.jpg',
        'badge': None,
    },
    {
        'id': 4,
        'nombre': 'Cilindro Abierto Para Residuos',
        'descripcion': 'Cilindro de acero de boca abierta especialmente diseñado para almacenamiento y transporte de residuos industriales sólidos. Disponible en varios colores para clasificación de residuos.',
        'usos': ['Residuos sólidos industriales', 'Chatarra y metales', 'Residuos de manufactura', 'Almacenamiento temporal de residuos'],
        'categoria': 'metal',
        'imagen': '/static/img/products/cilindro-metal-abierto-residuos.jpg',
        'badge': 'Mayor demanda',
    },
    {
        'id': 5,
        'nombre': 'Cilindro Abierto de Tapa Grande',
        'descripcion': 'Cilindro de acero con tapa desmontable de apertura grande. Robusto y duradero, ideal para productos de alta viscosidad o que requieren fácil acceso al interior.',
        'usos': ['Aceites y lubricantes', 'Grasas industriales', 'Pinturas y barnices', 'Productos petroquímicos'],
        'categoria': 'metal',
        'imagen': '/static/img/products/cilindro-metal-tapa-grande.jpg',
        'badge': None,
    },
    {
        'id': 6,
        'nombre': 'Cilindro Cerrado de Tapa Pequeña',
        'descripcion': 'Cilindro de acero hermético con tapa de rosca pequeña. Apto para aceites, lubricantes y productos petroquímicos. Garantiza máxima seguridad en el transporte de líquidos.',
        'usos': ['Aceites y lubricantes', 'Productos petroquímicos', 'Combustibles', 'Pinturas y solventes'],
        'categoria': 'metal',
        'imagen': '/static/img/products/cilindro-metal-cerrado.jpg',
        'badge': None,
    },
    {
        'id': 7,
        'nombre': 'Cilindro Abierto Sin Tapa',
        'descripcion': 'Cilindro de acero de boca completamente abierta. Versátil y resistente, ideal para almacenamiento de materiales sólidos, residuos industriales y uso como contenedor general.',
        'usos': ['Almacenamiento de materiales sólidos', 'Contenedor para residuos', 'Reciclaje industrial', 'Uso como contenedor general'],
        'categoria': 'metal',
        'imagen': '/static/img/products/cilindro-metal-sin-tapa.jpg',
        'badge': None,
    },
    {
        'id': 8,
        'nombre': 'Bidones Plásticos por Capacidad',
        'descripcion': 'Bidones plásticos de alta resistencia disponibles en distintas capacidades. Ideales para almacenamiento y transporte de líquidos y sólidos en procesos industriales.',
        'usos': ['Almacenamiento de aceites y lubricantes', 'Productos de limpieza industrial', 'Solventes y químicos', 'Uso industrial general'],
        'categoria': 'bidones',
        'imagen': '/static/img/products/bidon-plastico-capacidad.jpg',
        'badge': None,
    },
    {
        'id': 9,
        'nombre': 'Cilindros de Cartón por Capacidad',
        'descripcion': 'Cilindros de cartón multicapa disponibles en distintas capacidades. Ideales para el envasado de productos en polvo, granulados y sólidos secos. Ligeros y reutilizables.',
        'usos': ['Productos en polvo', 'Granulados industriales', 'Sólidos secos', 'Materiales de manufactura'],
        'categoria': 'bidones',
        'imagen': '/static/img/products/cilindro-carton-capacidad.jpg',
        'badge': None,
    },
]

SERVICIOS = [
    {
        'titulo': 'Gestión Integral de Residuos',
        'descripcion': 'Manejo completo de residuos sólidos industriales y comerciales conforme a la normativa ambiental peruana vigente (Ley N° 1278). Emitimos toda la documentación y certificados requeridos.',
        'icono': 'bi-recycle',
        'detalle': 'Gestionamos residuos peligrosos y no peligrosos con estricto cumplimiento de la normativa del MINAM y OEFA.',
    },
    {
        'titulo': 'Transporte de Residuos',
        'descripcion': 'Servicio de recolección y transporte de residuos peligrosos y no peligrosos con unidades debidamente equipadas, señalizadas y personal capacitado en manejo seguro.',
        'icono': 'bi-truck',
        'detalle': 'Contamos con unidades de transporte autorizadas por el MTC para el traslado de residuos peligrosos en Lima y provincias.',
    },
    {
        'titulo': 'Disposición Final',
        'descripcion': 'Disposición final de residuos en rellenos de seguridad autorizados y plantas de tratamiento certificadas. Garantizamos trazabilidad total del proceso.',
        'icono': 'bi-shield-check',
        'detalle': 'Trabajamos con instalaciones de disposición final debidamente autorizadas por las autoridades competentes.',
    },
    {
        'titulo': 'Compra de Residuos y Envases',
        'descripcion': 'Compramos tus residuos industriales: envases plásticos usados, cilindros metálicos, tanques IBC, galoneras y más. Evaluación técnica sin costo.',
        'icono': 'bi-cash-coin',
        'detalle': 'Ofrecemos precio justo por tus residuos aprovechables. Nos encargamos del recojo en tu empresa, sin costo adicional para volúmenes significativos.',
    },
]


@app.route('/')
def index():
    return render_template('index.html', productos=PRODUCTOS[:4], servicios=SERVICIOS[:3])


@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


@app.route('/servicios')
def servicios():
    return render_template('servicios.html', servicios=SERVICIOS)


@app.route('/productos')
def productos():
    categoria = request.args.get('categoria', 'todos')
    if categoria == 'todos':
        productos_filtrados = PRODUCTOS
    else:
        productos_filtrados = [p for p in PRODUCTOS if p['categoria'] == categoria]
    return render_template('productos.html', productos=productos_filtrados, categoria=categoria)


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        asunto = request.form.get('asunto', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        if not all([nombre, email, asunto, mensaje]):
            flash('Por favor completa todos los campos requeridos.', 'danger')
        else:
            flash('¡Mensaje enviado correctamente! Nos comunicaremos contigo a la brevedad.', 'success')
            return redirect(url_for('contacto'))

    return render_template('contacto.html')


@app.after_request
def set_cache_headers(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    else:
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return response


@app.route('/sitemap.xml')
def sitemap():
    base = 'https://www.operadorderesiduos.com.pe'
    now = datetime.utcnow().strftime('%Y-%m-%d')
    categorias = ['tanques', 'plastico', 'metal', 'bidones']
    urls = [
        {'loc': base + '/',            'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': base + '/nosotros',    'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': base + '/servicios',   'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': base + '/productos',   'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': base + '/contacto',    'priority': '0.8', 'changefreq': 'monthly'},
    ] + [{'loc': f'{base}/productos?categoria={c}', 'priority': '0.7', 'changefreq': 'weekly'} for c in categorias]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url><loc>{u["loc"]}</loc><lastmod>{now}</lastmod>'
        xml += f'<changefreq>{u["changefreq"]}</changefreq><priority>{u["priority"]}</priority></url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True)
