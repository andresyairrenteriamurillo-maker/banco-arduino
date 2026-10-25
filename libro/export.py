import json, importlib, glob, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p_base
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p[0-9][0-9]_*.py'))):
    importlib.import_module(os.path.basename(f)[:-3])
seen=set()
for p in p_base.PROJ:
    assert p['titulo'] not in seen, p['titulo']; seen.add(p['titulo'])
json.dump(p_base.PROJ, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'proyectos_libro.json'),'w'), ensure_ascii=False, indent=1)
print(len(p_base.PROJ), 'proyectos')
