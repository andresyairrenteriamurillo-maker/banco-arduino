import json,re
H='/home/claude/banco-arduino/index.html'
P=json.load(open('proyectos_libro.json'))
s=open(H).read()
a=s.index('/* ---- proyectos del libro'); b=s.index('function findLibrary(text){')
blk=s[a:b]
i=blk.index('LIB.push(...')
js=json.dumps(P,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
blk=blk[:i]+'LIB.push(...'+js+');\n'
s=s[:a]+blk+s[b:]
open(H,'w').write(s); print('embebidos',len(P))
