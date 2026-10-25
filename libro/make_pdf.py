import subprocess, json, re, os, sys
from pypdf import PdfReader, PdfWriter
D=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(D,'book')
def run(*a): subprocess.run(a,check=True,cwd=D)
run('python3','build_book.py')
run('node','render.js',B,'body')
r=PdfReader(os.path.join(B,'body.pdf')); pages={}
for n,pg in enumerate(r.pages,1):
    for k in re.findall(r'QZ(\w+?)QZ', pg.extract_text() or ''):
        pages.setdefault(k,n)
print('marcas',len(pages),'paginas',len(r.pages))
json.dump(pages,open(os.path.join(D,'paginas.json'),'w'))
run('python3','build_book.py','paginas.json')
run('node','render.js',B,'cover,body,back')
w=PdfWriter()
for f in ['cover','body','back']:
    for pg in PdfReader(os.path.join(B,f+'.pdf')).pages: w.add_page(pg)
w.add_metadata({'/Title':'Banco Arduino – Libro 2026-2027','/Author':'Ing. Jair Murillo','/Subject':'205 proyectos de Arduino paso a paso'})
out=os.path.join(B,'Libro-Banco-Arduino-2026-2027.pdf'); w.write(out)
print('listo',out,os.path.getsize(out)//1024,'KB')
