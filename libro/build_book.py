# -*- coding: utf-8 -*-
"""Genera el libro «Banco Arduino – Libro 2026-2027» en HTML (portada aparte + cuerpo).
Uso: python3 build_book.py [paginas.json]
"""
import json, re, html, os, glob, sys, collections
from PIL import Image, ImageChops
from contenido import *

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'book'); os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
P = json.load(open(os.path.join(D, 'proyectos_libro.json')))
PLANS = {}
for f in glob.glob(os.path.join(D, 'plans_*.json')):
    PLANS.update(json.load(open(f)))
PAGES = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else {}
SITE = 'https://andresyairrenteriamurillo-maker.github.io/banco-arduino/'
INST = open(os.path.join(D, 'institucion.txt')).read().strip() if os.path.exists(os.path.join(D, 'institucion.txt')) else ''
E = lambda s: html.escape(str(s), quote=False)


# ---------------------------------------------------------------- imágenes
def prep(src, dst, maxw=1250, q=82, pad=18):
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        return dst
    im = Image.open(src).convert('RGB')
    w, h = im.size
    inner = im.crop((4, 4, w - 4, h - 4))
    bg = Image.new('RGB', inner.size, (255, 255, 255))
    diff = ImageChops.difference(inner, bg).convert('L').point(lambda v: 255 if v > 26 else 0)
    bb = diff.getbbox()
    if bb:
        x0, y0, x1, y1 = bb
        im = inner.crop((max(0, x0 - pad), max(0, y0 - pad), min(inner.width, x1 + pad), min(inner.height, y1 + pad)))
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=q, optimize=True, progressive=True)
    return dst


def img(i, kind):
    src = os.path.join(D, 'img', f'p{i}_{kind}.png')
    if not os.path.exists(src):
        return ''
    return 'img/' + os.path.basename(prep(src, os.path.join(OUT, 'img', f'p{i}_{kind}.jpg')))


def catimg(t):
    src = os.path.join(D, 'img', f'cat_{t}.png')
    if not os.path.exists(src):
        return ''
    dst = os.path.join(OUT, 'img', f'cat_{t}.png')
    if not os.path.exists(dst):
        im = Image.open(src).convert('RGBA')
        bb = im.getbbox()
        if bb: im = im.crop(bb)
        im.save(dst)
    return f'img/cat_{t}.png'


# ---------------------------------------------------------------- código con colores
KW = r'void|int|long|float|bool|boolean|char|byte|const|unsigned|String|if|else|for|while|return|true|false|break|switch|case|HIGH|LOW|INPUT|OUTPUT|INPUT_PULLUP|static'
TOK = re.compile(r'(//[^\n]*)|("(?:[^"\\\n]|\\.)*")|(\'(?:[^\'\\\n]|\\.)\')|(#\w+)|\b(' + KW + r')\b|\b(\d+(?:\.\d+)?)\b')


def hl(code):
    out = []
    for line in code.rstrip('\n').split('\n'):
        pos, buf = 0, []
        for m in TOK.finditer(line):
            buf.append(E(line[pos:m.start()]))
            cls = ['c', 's', 's', 'p', 'k', 'n'][[g is not None for g in m.groups()].index(True)]
            buf.append(f'<span class="{cls}">{E(m.group(0))}</span>')
            pos = m.end()
        buf.append(E(line[pos:]))
        out.append('<span class="ln">' + (''.join(buf) or ' ') + '</span>')
    return ''.join(out)


# ---------------------------------------------------------------- utilidades
def mark(key):
    return f'<span class="mk">QZ{key}QZ</span>'


def pg(key):
    return str(PAGES.get(key, '000'))


def stars(n):
    return '★' * n + '☆' * (3 - n)


def plan_parts(t):
    h = PLANS.get(t, '')
    mats = []
    m = re.search(r'<div class="mats">(.*?)</div>', h, re.S)
    if m:
        mats = re.findall(r'<span>(.*?)</span>', m.group(1), re.S)
    steps = ''
    m = re.search(r'<ol class="steps">(.*?)</ol>', h, re.S)
    if m:
        steps = m.group(1)
        steps = re.sub(r'<i style="[^"]*"></i>', '', steps)
        steps = re.sub(r'<i></i>', '', steps)
        steps = re.sub(r' style="[^"]*"', '', steps)
    return mats, steps


def libs_of(code):
    out = []
    for inc in re.findall(r'#include\s*<([^>]+)>', code):
        v = LIBS.get(inc, inc)
        if v and v not in out:
            out.append(v)
    return out


ORDER = sorted(range(len(P)), key=lambda i: (CAT_ORDER.index(P[i]['cat']), i))
NUM = {i: n + 1 for n, i in enumerate(ORDER)}
BYCAT = collections.OrderedDict((c, [i for i in ORDER if P[i]['cat'] == c]) for c in CAT_ORDER)

# ---------------------------------------------------------------- escudo
ESCUDO_FILE = next((f for f in ['escudo.png', 'escudo.jpg', 'escudo.jpeg', 'escudo.svg'] if os.path.exists(os.path.join(D, f))), None)
if ESCUDO_FILE:
    import shutil
    shutil.copy(os.path.join(D, ESCUDO_FILE), os.path.join(OUT, 'img', ESCUDO_FILE))
    ESCUDO = f'<img class="escudo" src="img/{ESCUDO_FILE}" alt="Escudo de la institución">'
else:
    ESCUDO = '''<svg class="escudo" viewBox="0 0 120 140" aria-label="Escudo de la institución">
  <path d="M60 4 L112 20 V66 C112 102 88 124 60 136 C32 124 8 102 8 66 V20 Z" fill="#fff" stroke="#C9A227" stroke-width="5"/>
  <path d="M60 16 L100 28 V66 C100 95 82 112 60 122 C38 112 20 95 20 66 V28 Z" fill="#1F2D5C"/>
  <path d="M60 16 V122 M20 62 H100" stroke="#C9A227" stroke-width="2.5"/>
  <circle cx="40" cy="44" r="9" fill="#C9A227"/><rect x="70" y="36" width="20" height="16" rx="2" fill="#C9A227"/>
  <path d="M30 92 l10-12 10 12 M70 92 h20 M80 82 v20" stroke="#fff" stroke-width="3" fill="none"/>
  <text x="60" y="76" text-anchor="middle" fill="#fff" font-family="Inter" font-weight="800" font-size="11">ESCUDO</text></svg>'''

# ================================================================= CSS
CSS = r'''
@font-face{font-family:Inter}
:root{--ink:#16202E;--muted:#5B6878;--line:#D8DEE6;--soft:#F3F6FA;--navy:#1F2D5C;--gold:#C9A227;--rail-n:#3268C9;--rail-p:#D9473F;--info:#0D74CE;--warn:#B54708}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:Inter,'DejaVu Sans',sans-serif;color:var(--ink);font-size:10.4pt;line-height:1.48}
h1,h2,h3,h4{font-family:'Inter Display',Inter,sans-serif;line-height:1.15;margin:0}
p{margin:0 0 7pt}
b{font-weight:650}
.mk{position:absolute;font-size:3px;color:#fff;line-height:1}
.page{break-before:page}
.center{text-align:center}
.eyebrow{font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--muted)}
code,.mono{font-family:'DejaVu Sans Mono',monospace;font-size:.88em}
code{background:var(--soft);padding:0 3px;border-radius:3px}
ul,ol{margin:0 0 8pt;padding-left:17pt}
li{margin:1.5pt 0}

/* portadilla, créditos */
.titlepage{height:9.3in;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:14pt}
.titlepage .escudo{width:1.2in;height:auto}
.titlepage h1{font-size:34pt;font-weight:850;letter-spacing:-.02em}
.titlepage .sub{font-size:13pt;color:var(--muted);max-width:5in}
.titlepage .autor{font-size:13pt;font-weight:700;letter-spacing:.08em;margin-top:28pt}
.credits{height:9.3in;display:flex;flex-direction:column;justify-content:flex-end;font-size:9pt;color:var(--muted)}
.credits p{margin-bottom:5pt}

/* títulos de sección */
.sect h1{font-size:24pt;font-weight:850;margin:4pt 0 4pt;letter-spacing:-.01em}
.sect .lead{font-size:11.5pt;color:var(--muted);margin-bottom:14pt}
.sect h2{font-size:14.5pt;font-weight:800;margin:16pt 0 6pt;color:var(--navy)}
.sect h3{font-size:11.5pt;font-weight:750;margin:12pt 0 4pt}
.bar{height:5pt;width:46pt;background:var(--gold);border-radius:3pt;margin:6pt 0 8pt}
.box{border:1px solid var(--line);border-radius:7pt;padding:9pt 11pt;margin:8pt 0;break-inside:avoid;background:#fff}
.box h4{font-size:10.5pt;margin-bottom:4pt}
.box.tip{background:#FFF8E1;border-color:#F2D27A}
.box.warn{background:#FFF1EE;border-color:#F5B7A8}
.box.info{background:#EEF5FF;border-color:#B9D3F7}
.box.ok{background:#EEFAF1;border-color:#A9DDB8}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10pt}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8pt}
table{border-collapse:collapse;width:100%;font-size:9.4pt;margin:6pt 0 10pt;break-inside:avoid}
th,td{border:1px solid var(--line);padding:4pt 6pt;text-align:left;vertical-align:top}
th{background:var(--soft);font-weight:700}
.sw{display:inline-block;width:14pt;height:10pt;border-radius:2pt;border:1px solid #999;vertical-align:-1pt}
figure{margin:8pt 0;break-inside:avoid}
figure img{display:block;max-width:100%;margin:0 auto}
figcaption{font-size:8.5pt;color:var(--muted);text-align:center;margin-top:3pt}
pre.code{font-family:'DejaVu Sans Mono',monospace;font-size:8.1pt;line-height:1.42;background:#0F1726;color:#E6EDF3;border-radius:7pt;padding:9pt 10pt 9pt 8pt;white-space:pre-wrap;word-break:break-word;margin:6pt 0 10pt;counter-reset:ln}
pre.code .ln{display:block;padding-left:26pt;text-indent:-26pt}
pre.code .ln::before{counter-increment:ln;content:counter(ln);display:inline-block;width:20pt;margin-right:6pt;text-align:right;color:#5C6B80;text-indent:0}
pre.code .c{color:#7FA3C7;font-style:italic}.code .s{color:#A5E19B}.code .k{color:#FF9E7A;font-weight:600}.code .p{color:#D7A6FF}.code .n{color:#F7D774}

/* contenido */
.toc h2{font-size:12pt;margin:10pt 0 3pt;color:var(--navy)}
.toc .cols{columns:2;column-gap:18pt}
.toc .it{display:flex;gap:4pt;font-size:8.9pt;line-height:1.5;break-inside:avoid}
.toc .it .t{flex:0 1 auto}
.toc .it .d{flex:1;border-bottom:1px dotted #B9C2CE;transform:translateY(-3pt)}
.toc .it .n{flex:0 0 auto;font-variant-numeric:tabular-nums;color:var(--muted)}
.toc .ch{display:flex;gap:4pt;font-weight:750;font-size:10pt;margin:7pt 0 2pt;break-after:avoid}
.toc .ch .d{flex:1;border-bottom:1px dotted #B9C2CE;transform:translateY(-3pt)}

/* apertura de capítulo */
.chap{height:9.3in;display:flex;flex-direction:column;justify-content:space-between;padding:0;break-before:page}
.chap .top{background:var(--c);color:#fff;border-radius:14pt;padding:34pt 30pt 30pt;position:relative;overflow:hidden}
.chap .top::after{content:'';position:absolute;right:-40pt;top:-40pt;width:220pt;height:220pt;border-radius:50%;border:26pt solid rgba(255,255,255,.12)}
.chap .k{font-size:10pt;letter-spacing:.2em;text-transform:uppercase;opacity:.85;font-weight:700}
.chap h1{font-size:32pt;font-weight:850;margin:8pt 0 10pt;max-width:5.2in}
.chap .top p{font-size:12pt;max-width:5in;opacity:.95}
.chap ol{columns:2;column-gap:20pt;font-size:9.6pt;padding-left:0;list-style:none}
.chap ol li{break-inside:avoid;display:flex;gap:6pt;margin:2.5pt 0}
.chap ol li .n{color:var(--c);font-weight:800;min-width:22pt}
.chap ol li .s{color:#E0A100;margin-left:auto;font-size:8pt}

/* proyecto */
.proj{break-before:page}
.ph{border-left:6pt solid var(--c);padding:2pt 0 2pt 10pt;margin-bottom:8pt}
.ph .num{font-size:8.6pt;letter-spacing:.16em;text-transform:uppercase;font-weight:800;color:var(--c)}
.ph h2{font-size:20pt;font-weight:850;margin:2pt 0 3pt;letter-spacing:-.01em}
.ph .meta{font-size:8.8pt;color:var(--muted)}
.ph .meta .st{color:#E0A100;letter-spacing:1pt}
.idea{font-size:11pt;margin:6pt 0 8pt}
.top2{display:grid;grid-template-columns:1.55fr 1fr;gap:10pt;align-items:start}
.top2 figure{margin:0;border:1px solid var(--line);border-radius:8pt;padding:4pt;background:#fff}
.mat{background:var(--soft);border-radius:8pt;padding:8pt 10pt;font-size:9pt}
.mat h3,.proj h3{font-size:11.5pt;font-weight:800;margin:0 0 4pt}
.mat ul{padding-left:12pt;margin:0}
.mat .libs{margin-top:6pt;font-size:8.6pt}
.wire{border:1px solid var(--line);border-radius:8pt;padding:4pt;margin:9pt 0}
.wire img{max-height:3.25in}
.proj h3.sec{margin:12pt 0 5pt;display:flex;align-items:center;gap:6pt;break-after:avoid}
.proj h3.sec::before{content:attr(data-n);display:inline-grid;place-items:center;width:17pt;height:17pt;border-radius:50%;background:var(--c);color:#fff;font-size:9pt}
ol.steps{padding-left:0;list-style:none;counter-reset:st;margin:0;columns:2;column-gap:8pt}
.sect ol.steps{columns:1}
ol.steps>li{counter-increment:st;break-inside:avoid;display:block;border:1px solid var(--line);border-radius:7pt;padding:5pt 8pt 5pt 30pt;margin:0 0 5pt;position:relative;font-size:8.7pt;line-height:1.36}
ol.steps>li::before{content:counter(st);position:absolute;left:8pt;top:5pt;width:15pt;height:15pt;border-radius:4pt;background:var(--ink);color:#fff;font-size:8pt;font-weight:800;display:grid;place-items:center}
ol.steps .h{font-weight:750;font-size:9.8pt;margin-bottom:1pt}
ol.steps small{font-size:8.4pt}
ol.steps ul{margin:0;padding-left:13pt}
.two{display:grid;grid-template-columns:1fr 1fr;gap:9pt;margin-top:4pt}
.reto{border:2px dashed var(--c);border-radius:8pt;padding:8pt 11pt;margin-top:9pt;break-inside:avoid}
.reto b{color:var(--c)}
.notes li{font-size:9.2pt}
.check{list-style:none;padding-left:0}.check li::before{content:'☐ ';color:var(--muted)}

/* catálogo */
.cat{display:grid;grid-template-columns:1fr 1fr;gap:9pt}
.ccard{border:1px solid var(--line);border-radius:8pt;padding:8pt;display:grid;grid-template-columns:78pt 1fr;gap:8pt;break-inside:avoid;font-size:8.8pt;line-height:1.38}
.ccard img{width:78pt;height:78pt;object-fit:contain;background:var(--soft);border-radius:6pt}
.ccard h4{font-size:10pt;margin-bottom:2pt}
.ccard p{margin:0 0 3pt}
.ccard .pins{color:var(--muted)}
.lined{height:9.2in;background:repeating-linear-gradient(#fff 0 25pt,#C9D2DD 25pt 26pt)}
'''


# ================================================================= secciones fijas
def svg_ohm():
    return '''<svg viewBox="0 0 220 170" width="190"><path d="M110 10 L205 160 H15 Z" fill="#EEF5FF" stroke="#1F2D5C" stroke-width="3"/>
<path d="M58 95 H162 M110 95 V160" stroke="#1F2D5C" stroke-width="2.5"/>
<text x="110" y="78" text-anchor="middle" font-size="34" font-weight="800" fill="#D9473F" font-family="Inter">V</text>
<text x="80" y="140" text-anchor="middle" font-size="30" font-weight="800" fill="#0D74CE" font-family="Inter">I</text>
<text x="140" y="140" text-anchor="middle" font-size="30" font-weight="800" fill="#2F9E44" font-family="Inter">R</text></svg>'''


def svg_led():
    return '''<svg viewBox="0 0 420 150" width="100%"><g font-family="Inter" font-size="12" fill="#16202E">
<rect x="10" y="40" width="80" height="70" rx="8" fill="#1F4FA8"/><text x="50" y="70" text-anchor="middle" fill="#fff" font-weight="700">Arduino</text><text x="50" y="88" text-anchor="middle" fill="#fff">pin 13</text>
<path d="M90 60 H150" stroke="#D9473F" stroke-width="4"/>
<rect x="150" y="50" width="70" height="20" rx="6" fill="#E9D8B4" stroke="#8a6d3b"/><rect x="164" y="50" width="6" height="20" fill="#D9473F"/><rect x="176" y="50" width="6" height="20" fill="#D9473F"/><rect x="188" y="50" width="6" height="20" fill="#7B4A1E"/><rect x="204" y="50" width="5" height="20" fill="#C9A227"/>
<text x="185" y="40" text-anchor="middle">220 Ω</text>
<path d="M220 60 H270" stroke="#D9473F" stroke-width="4"/>
<path d="M270 42 V78 L300 60 Z" fill="#E5484D"/><path d="M300 42 V78" stroke="#16202E" stroke-width="4"/>
<path d="M286 36 l10 -12 M296 40 l10 -12" stroke="#E5484D" stroke-width="2"/>
<text x="285" y="100" text-anchor="middle">LED</text><text x="262" y="35">+</text><text x="305" y="35">−</text>
<path d="M300 60 H360 V130 H50 V110" stroke="#3268C9" stroke-width="4" fill="none"/>
<text x="205" y="146" text-anchor="middle">regresa por GND (0 V)</text></g></svg>'''


COLORS = [('Negro', '#111', 0), ('Café', '#7B4A1E', 1), ('Rojo', '#D9473F', 2), ('Naranja', '#F08C00', 3), ('Amarillo', '#F2C94C', 4),
          ('Verde', '#2F9E44', 5), ('Azul', '#1F6FEB', 6), ('Violeta', '#8E4EC6', 7), ('Gris', '#8A8F98', 8), ('Blanco', '#fff', 9)]


def fundamentos():
    rows = ''.join(f'<tr><td><span class="sw" style="background:{c}"></span> {n}</td><td>{d}</td><td>{"×" + str(10 ** d) if d < 7 else "—"}</td></tr>' for n, c, d in COLORS)
    return f'''
<section class="page sect">{mark('S_uso')}
<div class="eyebrow">Antes de empezar</div><h1>Cómo usar este libro</h1><div class="bar"></div>
<p class="lead">Este libro está pensado para que cualquier persona, aunque nunca haya conectado un cable, pueda armar sus propios proyectos con Arduino.</p>
<p>La <b>primera parte</b> explica lo básico: qué es la electricidad, cómo es la placa Arduino, cómo funciona la protoboard, cómo se escribe un programa y cómo se usa el simulador <b>Banco Arduino</b>. Léela con calma, en orden; solo toma una o dos clases.</p>
<p>La <b>segunda parte</b> trae <b>{len(P)} proyectos</b> organizados en {len(CAT_ORDER)} capítulos, de los más fáciles a los más completos. Todos los proyectos fueron armados y probados en el simulador. Cada uno trae:</p>
<div class="grid2">
<div class="box"><h4>🧰 Materiales</h4>La lista exacta de piezas, con las resistencias y cables que necesitas.</div>
<div class="box"><h4>🖼️ Dos ilustraciones</h4>La vista ilustrada del circuito armado y el plano de conexiones en la protoboard.</div>
<div class="box"><h4>🔌 Conexiones paso a paso</h4>Cada cable explicado: de qué pata sale y a qué pin o riel llega.</div>
<div class="box"><h4>💻 El programa</h4>El código completo con comentarios, listo para copiar en el Arduino IDE.</div>
<div class="box"><h4>💡 ¿Cómo funciona?</h4>La explicación sencilla de la idea del programa.</div>
<div class="box"><h4>🏆 Reto</h4>Una mejora para que pienses y lo hagas tuyo.</div>
</div>
<h2>Niveles de dificultad</h2>
<table><tr><th>Símbolo</th><th>Nivel</th><th>Para quién</th></tr>
<tr><td style="color:#E0A100">★☆☆</td><td>Básico</td><td>Primeros proyectos. Pocas piezas y programas cortos.</td></tr>
<tr><td style="color:#E0A100">★★☆</td><td>Intermedio</td><td>Usa sensores, variables y decisiones con <code>if</code>.</td></tr>
<tr><td style="color:#E0A100">★★★</td><td>Avanzado</td><td>Varias piezas, librerías, pantallas o cargas de 12 V.</td></tr></table>
<div class="box tip"><h4>Consejo para el estudiante</h4>Primero arma el proyecto en el simulador. Cuando funcione ahí, ármalo con piezas reales: así sabrás que el circuito y el programa están bien y, si algo falla, será un cable suelto.</div>
</section>

<section class="page sect">{mark('S_seg')}
<div class="eyebrow">Primero lo primero</div><h1>Seguridad en el laboratorio</h1><div class="bar"></div>
<p class="lead">La electrónica con Arduino es segura cuando se respetan unas reglas sencillas.</p>
<ol>
<li><b>Desconecta el USB antes de mover cables.</b> Arma o cambia el circuito siempre sin energía.</li>
<li><b>Revisa dos veces antes de conectar.</b> Un cable de 5V tocando GND es un corto circuito: el Arduino se calienta o se apaga.</li>
<li><b>Los LED siempre llevan resistencia</b> (220 Ω). Sin ella se queman en segundos.</li>
<li><b>Nunca conectes motores, bombas ni chapas directo a un pin.</b> Un pin da como máximo 20 mA; un motor pide cientos. Usa un transistor, un L298N o un relé.</li>
<li><b>12 V solo por el relé.</b> La fuente de 12 V nunca se une con el 5V del Arduino. Lo único que comparten, si hace falta, es el GND.</li>
<li><b>110 V no es para practicar.</b> Los proyectos de este libro usan máximo 12 V. Para controlar aparatos de la casa pide siempre la ayuda de un adulto o electricista.</li>
<li><b>El lector RFID va a 3.3 V</b>, no a 5 V.</li>
<li><b>Si algo huele a quemado o se calienta, desconecta el USB de inmediato</b> y avisa al docente.</li>
<li>Trabaja sobre una mesa seca, lejos de líquidos, y guarda las piezas en su caja al terminar.</li>
</ol>
<div class="box warn"><h4>⚠️ Regla de oro</h4>Si no estás seguro de una conexión, pruébala primero en el simulador Banco Arduino: él te avisa si hay un corto, una pieza al revés o un componente sin resistencia.</div>
</section>

<section class="page sect">{mark('S_elec')}
<div class="eyebrow">Fundamentos</div><h1>Electricidad básica</h1><div class="bar"></div>
<p class="lead">Para entender un circuito basta con tres ideas: voltaje, corriente y resistencia.</p>
<div class="grid3">
<div class="box info"><h4>Voltaje (V)</h4>Es la «fuerza» que empuja la electricidad, como la presión del agua en una manguera. Se mide en <b>voltios</b>. El Arduino trabaja con <b>5 V</b>.</div>
<div class="box info"><h4>Corriente (I)</h4>Es cuánta electricidad pasa, como el caudal de agua. Se mide en <b>amperios (A)</b> o <b>miliamperios (mA)</b>. Un LED usa unos 15 mA.</div>
<div class="box info"><h4>Resistencia (R)</h4>Es lo que frena la corriente, como estrechar la manguera. Se mide en <b>ohmios (Ω)</b>.</div>
</div>
<h2>La ley de Ohm</h2>
<div class="grid2" style="align-items:center"><div>{svg_ohm()}</div><div>
<p>Las tres se relacionan con una fórmula muy famosa:</p>
<p style="font-size:16pt;font-weight:800;text-align:center">V = I × R</p>
<p>Tapa con el dedo lo que quieres calcular en el triángulo: <b>I = V ÷ R</b> y <b>R = V ÷ I</b>.</p></div></div>
<div class="box tip"><h4>Ejemplo: ¿por qué 220 Ω para un LED?</h4>El pin da 5 V y el LED rojo «se queda» con unos 2 V. Quedan 3 V para la resistencia. Si queremos unos 15 mA (0,015 A): R = 3 ÷ 0,015 = 200 Ω. El valor comercial más cercano es <b>220 Ω</b>.</div>
<h2>Un circuito completo</h2>
<p>La electricidad necesita un camino de ida y vuelta: sale del pin, pasa por la resistencia y el LED, y regresa por <b>GND</b>. Si el camino se abre en cualquier punto, nada funciona.</p>
<figure>{svg_led()}<figcaption>Circuito básico: pin → resistencia → LED → GND.</figcaption></figure>
<h2>Potencia</h2>
<p>La potencia dice cuánta energía usa un aparato: <b>P = V × I</b>, en vatios (W). Una bomba de 12 V que consume 1 A usa 12 W.</p>
</section>

<section class="page sect">
<h2>Código de colores de las resistencias</h2>
<p>Las resistencias no traen el número escrito: lo indican con bandas de colores. Las dos primeras bandas son cifras, la tercera es el multiplicador (cuántos ceros) y la cuarta, dorada o plateada, la tolerancia.</p>
<table><tr><th>Color</th><th>Cifra</th><th>Multiplicador</th></tr>{rows}</table>
<div class="grid2">
<div class="box"><h4>220 Ω</h4><span class="sw" style="background:#D9473F"></span> <span class="sw" style="background:#D9473F"></span> <span class="sw" style="background:#7B4A1E"></span> <span class="sw" style="background:#C9A227"></span><br>rojo (2), rojo (2), café (×10) = 220 Ω. Para LED.</div>
<div class="box"><h4>10 kΩ</h4><span class="sw" style="background:#7B4A1E"></span> <span class="sw" style="background:#111"></span> <span class="sw" style="background:#F08C00"></span> <span class="sw" style="background:#C9A227"></span><br>café (1), negro (0), naranja (×1000) = 10 000 Ω. Para LDR y botones.</div>
</div>
<h2>Señales digitales y analógicas</h2>
<div class="grid2">
<div class="box"><h4>Digital</h4>Solo dos valores: <b>HIGH</b> (5 V, encendido, 1) o <b>LOW</b> (0 V, apagado, 0). Un botón, un LED o un relé son digitales.</div>
<div class="box"><h4>Analógica</h4>Muchos valores intermedios. El Arduino mide de 0 a 5 V y lo convierte en un número de <b>0 a 1023</b>. Una perilla o un sensor de luz son analógicos.</div>
</div>
<div class="box"><h4>PWM: la «falsa» salida analógica</h4>Los pines con el símbolo <b>~</b> (3, 5, 6, 9, 10 y 11) pueden encenderse y apagarse muy rápido. Con <code>analogWrite(pin, 0…255)</code> se controla qué parte del tiempo están encendidos: así se cambia el brillo de un LED o la velocidad de un motor.</div>
</section>

<section class="page sect">{mark('S_ard')}
<div class="eyebrow">Fundamentos</div><h1>La placa Arduino UNO y la protoboard</h1><div class="bar"></div>
<p class="lead">El Arduino es un pequeño computador que lee sensores y controla luces, sonidos y motores según el programa que le escribimos.</p>
<figure><img src="{'img/empty3d.jpg'}" style="max-height:3.2in"><figcaption>Arduino UNO y protoboard, tal como se ven en el simulador Banco Arduino.</figcaption></figure>
<table>
<tr><th>Parte</th><th>Para qué sirve</th></tr>
<tr><td><b>Pines digitales D0–D13</b></td><td>Entradas o salidas de HIGH/LOW. D0 y D1 los usa el USB: evítalos. Los que tienen <b>~</b> hacen PWM.</td></tr>
<tr><td><b>Pines analógicos A0–A5</b></td><td>Leen voltajes de 0 a 5 V como números de 0 a 1023. A4 (SDA) y A5 (SCL) también sirven para pantallas I2C.</td></tr>
<tr><td><b>5V y 3.3V</b></td><td>Salidas de energía para los sensores.</td></tr>
<tr><td><b>GND</b></td><td>Tierra o negativo (0 V). Hay tres y están unidos.</td></tr>
<tr><td><b>Conector USB</b></td><td>Lleva el programa desde el computador y da energía de 5 V.</td></tr>
<tr><td><b>Jack de alimentación</b></td><td>Para una fuente o batería de 7 a 12 V cuando no hay USB.</td></tr>
<tr><td><b>Botón RESET</b></td><td>Reinicia el programa desde el principio.</td></tr>
<tr><td><b>LED «L»</b></td><td>Conectado al pin 13: sirve para hacer la primera prueba sin piezas.</td></tr>
</table>
<h2>La protoboard</h2>
<div class="grid2" style="align-items:center"><figure><img src="img/empty2d.jpg"><figcaption>Plano de la protoboard y el Arduino.</figcaption></figure>
<div><p>La protoboard tiene agujeros unidos por dentro con láminas metálicas:</p><ul>
<li><b>Columnas numeradas (1, 2, 3…)</b>: los 5 agujeros de una columna (a–e o f–j) están unidos.</li>
<li><b>La canal del medio</b> separa las dos mitades: ahí se montan los chips y módulos.</li>
<li><b>Rieles</b> (línea roja + y azul −): recorren todo el tablero y reparten 5V y GND.</li></ul>
<p>Por eso cada pata de un componente debe ir en una <b>columna distinta</b>; si dos patas quedan en la misma columna, quedan unidas (en corto).</p></div></div>
</section>

<section class="page sect">{mark('S_prog')}
<div class="eyebrow">Fundamentos</div><h1>Programar el Arduino</h1><div class="bar"></div>
<p class="lead">Un programa de Arduino (sketch) siempre tiene dos partes.</p>
<pre class="code">{hl('''// Mi primer programa: parpadear el LED del pin 13
void setup() {             // se ejecuta UNA vez al encender
  pinMode(13, OUTPUT);     // el pin 13 será una salida
}

void loop() {              // se repite PARA SIEMPRE
  digitalWrite(13, HIGH);  // enciende
  delay(1000);             // espera 1 segundo
  digitalWrite(13, LOW);   // apaga
  delay(1000);
}''')}</pre>
<h2>Las instrucciones que más vas a usar</h2>
<table>
<tr><th>Instrucción</th><th>Qué hace</th><th>Ejemplo</th></tr>
<tr><td><code>pinMode(pin, modo)</code></td><td>Define si un pin es salida o entrada.</td><td><code>pinMode(2, INPUT_PULLUP);</code></td></tr>
<tr><td><code>digitalWrite(pin, v)</code></td><td>Pone un pin en HIGH o LOW.</td><td><code>digitalWrite(13, HIGH);</code></td></tr>
<tr><td><code>digitalRead(pin)</code></td><td>Lee HIGH o LOW.</td><td><code>if (digitalRead(2) == LOW)</code></td></tr>
<tr><td><code>analogRead(pin)</code></td><td>Lee de 0 a 1023.</td><td><code>int v = analogRead(A0);</code></td></tr>
<tr><td><code>analogWrite(pin, v)</code></td><td>PWM de 0 a 255 (pines ~).</td><td><code>analogWrite(9, 128);</code></td></tr>
<tr><td><code>delay(ms)</code></td><td>Espera en milisegundos.</td><td><code>delay(500);</code></td></tr>
<tr><td><code>millis()</code></td><td>Tiempo desde que encendió.</td><td><code>if (millis() - t > 1000)</code></td></tr>
<tr><td><code>tone(pin, Hz, ms)</code></td><td>Toca una nota en el zumbador.</td><td><code>tone(8, 440, 200);</code></td></tr>
<tr><td><code>map(v, a, b, c, d)</code></td><td>Cambia de escala.</td><td><code>map(v, 0, 1023, 0, 180)</code></td></tr>
<tr><td><code>Serial.println(x)</code></td><td>Envía un mensaje al monitor serie.</td><td><code>Serial.println("Hola");</code></td></tr>
<tr><td><code>random(a, b)</code></td><td>Número al azar de a hasta b−1.</td><td><code>random(1, 7)</code></td></tr>
</table>
<h2>Variables, decisiones y repeticiones</h2>
<pre class="code">{hl('''int contador = 0;              // variable entera
float temperatura = 24.5;      // número con decimales
bool encendido = false;        // verdadero o falso
String nombre = "Ana";         // texto

if (contador > 10) {           // decisión
  Serial.println("Mayor que 10");
} else {
  Serial.println("Todavía no");
}

for (int i = 0; i < 5; i++) {  // repetir 5 veces
  tone(8, 440 + i * 100, 100);
  delay(150);
}''')}</pre>
<div class="box tip"><h4>Reglas de escritura</h4>Cada instrucción termina en punto y coma <code>;</code>. Las llaves <code>{{ }}</code> agrupan instrucciones. Mayúsculas y minúsculas importan: <code>HIGH</code> no es lo mismo que <code>high</code>. Lo que va después de <code>//</code> es un comentario: el Arduino lo ignora.</div>
</section>

<section class="page sect">{mark('S_ide')}
<div class="eyebrow">Fundamentos</div><h1>Del computador al Arduino</h1><div class="bar"></div>
<h2>Subir un programa con el Arduino IDE</h2>
<ol class="steps">
<li><div class="h">Instala el Arduino IDE</div>Descárgalo gratis de <b>arduino.cc/en/software</b> e instálalo.</li>
<li><div class="h">Conecta el Arduino</div>Usa el cable USB. Se enciende el LED «ON».</li>
<li><div class="h">Elige la placa</div>Menú <b>Herramientas → Placa → Arduino AVR Boards → Arduino Uno</b>.</li>
<li><div class="h">Elige el puerto</div><b>Herramientas → Puerto</b> y selecciona el que dice COM (Windows) o /dev/tty (Mac/Linux).</li>
<li><div class="h">Escribe o pega el programa</div>Copia el código del proyecto en la ventana del IDE.</li>
<li><div class="h">Verifica</div>Pulsa el botón ✓. Si hay errores, aparecen abajo en rojo con el número de línea.</li>
<li><div class="h">Sube</div>Pulsa el botón → (Subir). Las luces TX y RX parpadean y aparece «Subido».</li>
<li><div class="h">Abre el monitor serie</div>Si el programa usa <code>Serial</code>, abre <b>Herramientas → Monitor serie</b> y elige <b>9600 baudios</b>.</li>
</ol>
<h2>Instalar librerías</h2>
<p>Algunos proyectos usan librerías (por ejemplo, para la pantalla, el teclado o el lector de huellas). Se instalan una sola vez:</p>
<ol><li>Menú <b>Herramientas → Administrar bibliotecas</b> (o el ícono de libros a la izquierda).</li><li>Escribe el nombre de la librería en el buscador.</li><li>Pulsa <b>Instalar</b>. Si pregunta por dependencias, elige <b>Instalar todo</b>.</li></ol>
<table><tr><th>Librería a buscar</th><th>Para</th></tr>
<tr><td>LiquidCrystal I2C</td><td>Pantalla LCD 16×2 con módulo I2C</td></tr>
<tr><td>Keypad</td><td>Teclado matricial 4×4</td></tr>
<tr><td>MFRC522</td><td>Lector de tarjetas RFID RC522</td></tr>
<tr><td>Adafruit Fingerprint Sensor Library</td><td>Lector de huellas R307 / AS608</td></tr>
<tr><td>DHT sensor library</td><td>Sensor de temperatura y humedad DHT11</td></tr>
<tr><td>Adafruit SSD1306 y Adafruit GFX</td><td>Pantalla OLED</td></tr>
<tr><td>Servo</td><td>Servomotores (ya viene instalada)</td></tr></table>
<div class="box info"><h4>Registrar huellas en el lector</h4>Antes de usar el lector de huellas, abre <b>Archivo → Ejemplos → Adafruit Fingerprint Sensor Library → enroll</b>, súbelo y sigue las instrucciones del monitor serie: escribe el número (1, 2, 3…) y pon el dedo dos veces. Ese número es el que devuelve <code>leerHuella()</code> en los proyectos.</div>
</section>

<section class="page sect">{mark('S_sim')}
<div class="eyebrow">Fundamentos</div><h1>El simulador Banco Arduino</h1><div class="bar"></div>
<p class="lead">Todos los proyectos de este libro están dentro del simulador. Se puede usar en el computador, la tableta o el celular, incluso sin internet después de abrirlo la primera vez.</p>
<div class="box ok"><h4>Dirección del simulador</h4><b>{SITE}</b></div>
<ol class="steps">
<li><div class="h">Busca el proyecto</div>Entra a <b>📚 Proyectos</b>, escribe su nombre (por ejemplo «chapa con huella») o filtra por categoría.</li>
<li><div class="h">Elige cómo armarlo</div><b>🧩 Armarlo yo, con guía</b> pone las piezas sin cables y te marca con ✓ cada conexión correcta. <b>👀 Ver armado completo</b> lo deja listo.</li>
<li><div class="h">Revisa el circuito</div>El panel <b>Revisión del circuito</b> avisa si falta un cable, si una pieza está al revés o si hay un corto.</li>
<li><div class="h">Ejecuta el programa</div>Pulsa <b>▶ Ejecutar</b>. Las luces, la pantalla, el zumbador y los servos se mueven como en la vida real, y el monitor serie muestra los mensajes.</li>
<li><div class="h">Interactúa con los sensores</div>En el panel <b>Componentes</b> cada sensor tiene su control: botones, deslizadores, huellas, tarjetas o teclas.</li>
<li><div class="h">Mira la vista ilustrada</div>La pestaña <b>Vista ilustrada</b> muestra el circuito en 3D con etiquetas, y Chispa, el robot guía, te lo explica paso a paso.</li>
</ol>
<div class="box tip"><h4>Para el docente</h4>En el modo <b>🧑‍🏫 Docente</b> (con PIN) se pueden crear proyectos nuevos, editarlos y exportarlos para compartirlos con otros computadores.</div>
</section>
'''


def catalogo():
    cards = ''.join(f'''<div class="ccard">{f'<img src="{catimg(t)}">' if catimg(t) else '<div></div>'}<div><h4>{E(n)}</h4><p>{E(d)}</p><p class="pins"><b>Conexión:</b> {E(pi)}</p><p><b>Ojo:</b> {E(tip)}</p></div></div>'''
                    for t, n, d, pi, tip in CATALOGO)
    return f'''<section class="page sect">{mark('S_cat')}<div class="eyebrow">Fundamentos</div><h1>Catálogo de componentes</h1><div class="bar"></div>
<p class="lead">Estas son las piezas que aparecen en los proyectos. Cada ficha dice para qué sirve y cómo se conecta.</p>
<div class="cat">{cards}</div></section>'''


def kit():
    need = collections.Counter()
    names = {t: n for t, n, *_ in CATALOGO}
    for p in P:
        c = collections.Counter(x['tipo'] for x in p['componentes'])
        for k, v in c.items():
            need[k] = max(need[k], v)
    uses = collections.Counter(t for p in P for t in set(c['tipo'] for c in p['componentes']))
    rows = ''.join(f'<tr><td>{E(names.get(k, k))}</td><td style="text-align:center">{need[k]}</td><td style="text-align:center">{uses[k]}</td></tr>'
                   for k in sorted(need, key=lambda k: -uses[k]) if k in names)
    return f'''<section class="page sect">{mark('S_kit')}<div class="eyebrow">Anexo</div><h1>Materiales para el kit</h1><div class="bar"></div>
<p class="lead">Con estas piezas se pueden armar todos los proyectos del libro. La columna «cantidad» es lo máximo que usa un solo proyecto.</p>
<table><tr><th>Componente</th><th>Cantidad</th><th>Proyectos que lo usan</th></tr>{rows}
<tr><td>Arduino UNO con cable USB</td><td style="text-align:center">1</td><td style="text-align:center">{len(P)}</td></tr>
<tr><td>Protoboard de 830 puntos</td><td style="text-align:center">1</td><td style="text-align:center">{len(P)}</td></tr>
<tr><td>Resistencias de 220 Ω y 10 kΩ</td><td style="text-align:center">10 c/u</td><td style="text-align:center">—</td></tr>
<tr><td>Cables macho-macho y macho-hembra</td><td style="text-align:center">40 c/u</td><td style="text-align:center">—</td></tr></table></section>'''


def anexos():
    probs = ''.join(f'<div class="box"><h4>{E(q)}</h4>{E(a)}</div>' for q, a in PROBLEMAS)
    glos = ''.join(f'<tr><td><b>{E(t)}</b></td><td>{E(d)}</td></tr>' for t, d in sorted(GLOSARIO, key=lambda x: x[0].lower()))
    return f'''<section class="page sect">{mark('S_prob')}<div class="eyebrow">Anexo</div><h1>Solución de problemas</h1><div class="bar"></div>
<p class="lead">Cuando algo no funciona casi siempre es un cable, un pin o una librería. Revisa esta lista antes de cambiar piezas.</p>{probs}</section>
<section class="page sect">{mark('S_glos')}<div class="eyebrow">Anexo</div><h1>Glosario</h1><div class="bar"></div><table>{glos}</table></section>
{kit()}
<section class="page sect">{mark('S_notas')}<div class="eyebrow">Anexo</div><h1>Mis notas</h1><div class="bar"></div><div class="lined"></div></section>
<section class="page sect"><div class="lined" style="height:9.6in"></div></section>'''


# ================================================================= proyectos
def proyecto(i):
    p = P[i]; n = NUM[i]; color = CAT_INFO[p['cat']][0]
    mats, steps = plan_parts(p['titulo'])
    i3, i2 = img(i, '3d'), img(i, '2d')
    libs = libs_of(p['codigo'])
    types = []
    for c in p['componentes']:
        if c['tipo'] in SIM_TEST and c['tipo'] not in types:
            types.append(c['tipo'])
    sim = ''.join(f'<li>{E(SIM_TEST[t])}</li>' for t in types)
    usa_serial = 'Serial.' in p['codigo']
    mats_html = ''.join(f'<li>{m}</li>' for m in mats) if mats else ''.join(f'<li>{E(c["nombre"])}</li>' for c in p['componentes'])
    notas = p.get('notas') or []
    return f'''
<section class="proj" style="--c:{color}">{mark('P' + str(n))}
<header class="ph"><div class="num">Proyecto {n} · {E(p['cat'])}</div><h2>{E(p['titulo'])}</h2>
<div class="meta"><span class="st">{stars(p['nivel'])}</span> {NIVEL[p['nivel']]} · Tiempo: {TIEMPO[p['nivel']]}</div></header>
<p class="idea">{E(p['idea'])}</p>
<div class="top2"><figure>{f'<img src="{i3}">' if i3 else ''}<figcaption>Así se ve armado (vista ilustrada del simulador)</figcaption></figure>
<aside class="mat"><h3>🧰 Materiales</h3><ul>{mats_html}</ul>
{('<div class="libs"><b>Librerías:</b> ' + '; '.join(E(l) for l in libs) + '</div>') if libs else ''}</aside></div>
{f'<figure class="wire"><img src="{i2}"><figcaption>Plano de conexiones: sigue los colores de los cables.</figcaption></figure>' if i2 else ''}
<h3 class="sec" data-n="1">Conexiones paso a paso</h3>
<ol class="steps">{steps}</ol>
<h3 class="sec" data-n="2">El programa</h3>
<pre class="code">{hl(p['codigo'])}</pre>
<div class="two">
<div class="box info"><h4>💡 ¿Cómo funciona?</h4>{E(p['explica'])}</div>
<div class="box ok"><h4>✅ Pruébalo</h4><b>En el simulador:</b> pulsa ▶ Ejecutar.{f'<ul style="margin:3pt 0 4pt">{sim}</ul>' if sim else ' '}
<b>Con piezas reales:</b> sube el programa{' y abre el monitor serie a 9600' if usa_serial else ''}.</div>
</div>
{('<div class="box tip"><h4>⚠️ Ten en cuenta</h4><ul class="notes" style="margin:0">' + ''.join(f'<li>{E(x)}</li>' for x in notas) + '</ul></div>') if notas else ''}
<div class="reto"><b>🏆 Reto:</b> {E(p['reto'])}</div>
</section>'''


def capitulo(k, cat):
    color, desc = CAT_INFO[cat]
    items = ''.join(f'<li><span class="n">{NUM[i]}</span><span>{E(P[i]["titulo"])}</span><span class="s">{stars(P[i]["nivel"])}</span></li>' for i in BYCAT[cat])
    return f'''<section class="chap" style="--c:{color}">{mark('C' + str(k))}
<div class="top"><div class="k">Capítulo {k}</div><h1>{E(cat)}</h1><p>{E(desc)}</p></div>
<div><div class="eyebrow" style="margin-bottom:6pt">En este capítulo · {len(BYCAT[cat])} proyectos</div><ol>{items}</ol></div></section>'''


def toc():
    fixed = [('S_uso', 'Cómo usar este libro'), ('S_seg', 'Seguridad en el laboratorio'), ('S_elec', 'Electricidad básica'),
             ('S_ard', 'La placa Arduino UNO y la protoboard'), ('S_prog', 'Programar el Arduino'), ('S_ide', 'Del computador al Arduino'),
             ('S_sim', 'El simulador Banco Arduino'), ('S_cat', 'Catálogo de componentes')]
    an = [('S_prob', 'Solución de problemas'), ('S_glos', 'Glosario'), ('S_kit', 'Materiales para el kit'), ('S_notas', 'Mis notas')]
    it = lambda k, t: f'<div class="it"><span class="t">{E(t)}</span><span class="d"></span><span class="n">{pg(k)}</span></div>'
    out = f'<section class="page sect toc">{mark("S_toc")}<div class="eyebrow">Índice</div><h1>Contenido</h1><div class="bar"></div>'
    out += '<h2>Primera parte · Fundamentos</h2>' + ''.join(it(k, t) for k, t in fixed)
    out += '<h2>Segunda parte · Proyectos</h2><div class="cols">'
    for k, cat in enumerate(CAT_ORDER, 1):
        out += f'<div class="ch"><span>{k}. {E(cat)}</span><span class="d"></span><span class="n">{pg("C" + str(k))}</span></div>'
        out += ''.join(it('P' + str(NUM[i]), f'{NUM[i]}. {P[i]["titulo"]}') for i in BYCAT[cat])
    out += '</div><h2>Anexos</h2>' + ''.join(it(k, t) for k, t in an) + '</section>'
    return out


def presentacion():
    return f'''<section class="page sect">{mark('S_pres')}<div class="eyebrow">Presentación</div><h1>Bienvenidos al mundo Arduino</h1><div class="bar"></div>
<p class="lead">Este libro nace en el aula, para el aula.</p>
<p>Hoy la tecnología está en todas partes: en la puerta que se abre con una huella, en el semáforo de la esquina, en la alarma de la casa y en el celular que llevamos en el bolsillo. Detrás de todos esos aparatos hay una misma idea: <b>sensores que miden, un pequeño computador que decide y actuadores que hacen algo</b>. Con una placa Arduino, unos cuantos componentes y curiosidad, cualquier estudiante puede construir esas mismas soluciones.</p>
<p>Aquí encontrarás <b>{len(P)} proyectos</b> sencillos y prácticos, inspirados en problemas reales de la casa, el colegio y la comunidad: desde encender el primer LED hasta construir una chapa eléctrica con lector de huellas, un control de asistencia con tarjetas RFID, un sistema de riego, una alarma contra gas o un robot que esquiva obstáculos.</p>
<p>Cada proyecto está explicado <b>paso a paso</b>: qué piezas necesitas, cómo se conecta cada cable, el programa completo con comentarios y una explicación sencilla de cómo funciona. Todos se pueden practicar primero en el simulador <b>Banco Arduino</b>, para equivocarse sin miedo, y luego armarse con piezas reales.</p>
<p>La invitación es a no quedarse en copiar: modifica, prueba, rompe (en el simulador) y vuelve a armar. Los <b>retos</b> al final de cada proyecto están para eso. Equivocarse es parte de aprender, y cada error resuelto es un paso más hacia convertirte en creador de tecnología.</p>
<p style="margin-top:22pt"><b>Ing. Jair Murillo</b><br><span style="color:var(--muted)">Docente · Libro 2026 – 2027</span></p>
<div class="box ok" style="margin-top:22pt"><h4>Este libro es de:</h4><div style="border-bottom:1px solid #9aa;height:22pt"></div><div style="display:flex;gap:16pt;margin-top:8pt"><span style="flex:1">Grado: <span style="display:inline-block;border-bottom:1px solid #9aa;width:70%"></span></span><span style="flex:1">Año: <span style="display:inline-block;border-bottom:1px solid #9aa;width:70%"></span></span></div></div>
</section>'''


def body():
    head = f'''<section class="titlepage">{ESCUDO}{f'<div class="eyebrow">{E(INST)}</div>' if INST else ''}
<div class="eyebrow">Libro 2026 – 2027</div><h1>Banco Arduino</h1>
<div class="sub">{len(P)} proyectos de electrónica y programación explicados paso a paso para estudiantes</div>
<div class="autor">ING. JAIR MURILLO</div></section>
<section class="page credits"><p><b>Banco Arduino · Libro 2026 – 2027</b></p>
<p>Autor: Ing. Jair Murillo{(' · ' + E(INST)) if INST else ''}</p>
<p>Ilustraciones de circuitos generadas con el simulador Banco Arduino.</p>
<p>Simulador: {SITE}</p>
<p>Material educativo de uso en el aula. Se permite imprimirlo y fotocopiarlo con fines educativos citando al autor.</p>
<p>Arduino® es una marca registrada de Arduino SA. Este libro no está afiliado a Arduino SA.</p></section>'''
    out = head + presentacion() + toc() + fundamentos() + catalogo()
    for k, cat in enumerate(CAT_ORDER, 1):
        if os.environ.get('PREVIEW') and k > 1 and cat != 'Seguridad y control de acceso': continue
        lst = BYCAT[cat][:int(os.environ.get('PREVIEW'))] if os.environ.get('PREVIEW') else BYCAT[cat]
        out += capitulo(k, cat) + ''.join(proyecto(i) for i in lst)
    out += anexos()
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Banco Arduino – Libro 2026-2027</title><style>{CSS}</style></head><body>{out}</body></html>'


def cover():
    hs = os.path.join(D, 'img', 'p%d_3d.png' % next(i for i in range(len(P)) if P[i]['titulo'] == 'Chapa eléctrica con huella'))
    if not os.path.exists(hs): hs = os.path.join(D, 'c3d.png')
    hero = 'img/' + os.path.basename(prep(hs, os.path.join(OUT, 'img', 'hero.jpg'), maxw=1500, q=88))
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}
@page{{size:Letter;margin:0}}
body{{width:8.5in;height:11in;overflow:hidden}}
.cv{{position:relative;width:8.5in;height:11in;background:#1F2D5C;color:#fff;overflow:hidden}}
.cv .grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:22pt 22pt}}
.cv .ring{{position:absolute;right:-1.6in;top:-1.4in;width:5.2in;height:5.2in;border-radius:50%;border:34pt solid rgba(201,162,39,.18)}}
.cv .in{{position:absolute;inset:0.6in 0.65in;display:flex;flex-direction:column;align-items:center;text-align:center}}
.cv .escudo{{width:1.25in;height:auto;filter:drop-shadow(0 6pt 12pt rgba(0,0,0,.35))}}
.cv .inst{{font-size:11pt;letter-spacing:.16em;text-transform:uppercase;font-weight:700;margin-top:10pt;opacity:.9}}
.cv .yr{{margin-top:16pt;display:inline-block;background:#C9A227;color:#1F2D5C;font-weight:850;letter-spacing:.18em;font-size:11pt;padding:6pt 16pt;border-radius:99pt}}
.cv h1{{font-size:58pt;font-weight:900;letter-spacing:-.03em;margin-top:14pt;line-height:1}}
.cv .sub{{font-size:14.5pt;opacity:.92;max-width:5.6in;margin-top:10pt;line-height:1.35}}
.cv .card{{margin-top:22pt;background:#fff;border-radius:16pt;padding:8pt;box-shadow:0 14pt 30pt rgba(0,0,0,.35);width:6.4in}}
.cv .card img{{width:100%;display:block;border-radius:10pt}}
.cv .tags{{display:flex;gap:7pt;flex-wrap:wrap;justify-content:center;margin-top:16pt}}
.cv .tags span{{border:1px solid rgba(255,255,255,.35);border-radius:99pt;padding:3pt 10pt;font-size:9.5pt}}
.cv .au{{margin-top:auto;font-size:17pt;font-weight:850;letter-spacing:.14em}}
.cv .au small{{display:block;font-size:9.5pt;font-weight:500;letter-spacing:.1em;opacity:.8;margin-top:4pt}}
</style></head><body><div class="cv"><div class="grid"></div><div class="ring"></div><div class="in">
{ESCUDO}{f'<div class="inst">{E(INST)}</div>' if INST else ''}
<div class="yr">LIBRO 2026 – 2027</div>
<h1>Banco Arduino</h1>
<div class="sub">{len(P)} proyectos de electrónica y programación<br>explicados paso a paso, con ilustraciones, conexiones y código</div>
<div class="card"><img src="{hero}"></div>
<div class="tags"><span>Lector de huellas</span><span>Chapas eléctricas</span><span>RFID</span><span>Sensores</span><span>Robótica</span><span>Domótica</span></div>
<div class="au">ING. JAIR MURILLO<small>DOCENTE · AUTOR</small></div>
</div></div></body></html>'''


def back():
    cats = ''.join(f'<span>{E(c)}</span>' for c in CAT_ORDER)
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}
@page{{size:Letter;margin:0}}
body{{width:8.5in;height:11in;overflow:hidden}}
.bk{{width:8.5in;height:11in;background:#1F2D5C;color:#fff;padding:1in 0.9in;display:flex;flex-direction:column;gap:14pt}}
.bk h2{{font-size:24pt;font-weight:850}}
.bk p{{font-size:12pt;line-height:1.55;opacity:.95}}
.bk .tags{{display:flex;flex-wrap:wrap;gap:6pt}}
.bk .tags span{{border:1px solid rgba(255,255,255,.35);border-radius:99pt;padding:3pt 10pt;font-size:9.5pt}}
.bk .ft{{margin-top:auto;display:flex;align-items:center;gap:14pt}}
.bk .escudo{{width:0.9in;height:auto}}
</style></head><body><div class="bk">
<h2>Aprende electrónica construyendo</h2>
<p>{len(P)} proyectos para armar con Arduino: luces, sonidos, sensores, pantallas, motores, lectores de huellas, chapas eléctricas, tarjetas RFID, domótica, juegos y robótica.</p>
<p>Cada proyecto incluye la lista de materiales, la vista ilustrada del circuito, el plano de conexiones en la protoboard, las conexiones explicadas cable por cable, el programa completo con comentarios, cómo funciona, cómo probarlo y un reto para seguir aprendiendo.</p>
<p>Todos los proyectos están dentro del simulador <b>Banco Arduino</b>, para practicarlos en el computador, la tableta o el celular antes de armarlos con piezas reales.</p>
<div class="tags">{cats}</div>
<div class="ft">{ESCUDO}<div><b style="font-size:14pt;letter-spacing:.1em">ING. JAIR MURILLO</b><br><span style="opacity:.8">Libro 2026 – 2027 · {SITE}</span></div></div>
</div></body></html>'''


if __name__ == '__main__':
    for f in ['empty3d', 'empty2d']:
        src = os.path.join(D, 'img', f + '.png')
        if os.path.exists(src): prep(src, os.path.join(OUT, 'img', f + '.jpg'), maxw=1400)
    open(os.path.join(OUT, 'body.html'), 'w').write(body())
    open(os.path.join(OUT, 'cover.html'), 'w').write(cover())
    open(os.path.join(OUT, 'back.html'), 'w').write(back())
    print('ok', len(P), 'proyectos;', 'páginas conocidas:', len(PAGES))
