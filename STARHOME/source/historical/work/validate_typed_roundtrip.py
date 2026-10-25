from read_typed import *
import hashlib
g=MappedGenerator();g.install_managed_resolver()
r=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo\StarHome_Data')
e=UnityPy.load(str(r/'globalgamemanagers.assets'),str(r/'sharedassets1.assets'));e.typetree_generator=g
ids=[11150,11154,11231,11500,11765,11785]
rows=[]
for o in e.objects:
    if not o.assets_file.name.endswith('sharedassets1.assets') or o.path_id not in ids:continue
    old=o.get_raw_data();tree=o.read_typetree();o.save_typetree(tree);new=o.get_raw_data()
    row={'path_id':o.path_id,'original_bytes':len(old),'rebuilt_bytes':len(new),'byte_identical':old==new}
    if old!=new:row['first_difference']=next((i for i,(a,b) in enumerate(zip(old,new)) if a!=b),min(len(old),len(new)))
    rows.append(row)
Path('work/prototype_evidence/typed_roundtrip.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
assert all(r['byte_identical'] for r in rows)
