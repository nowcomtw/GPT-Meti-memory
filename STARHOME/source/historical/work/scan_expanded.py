from read_typed import *
from odin_context import parse_odin
import re, collections
W=Path('work/expanded_021');W.mkdir(exist_ok=True)
g=MappedGenerator();g.install_managed_resolver()
D=Path('work/native_test_0.2.0/StarHome/StarHome_Data')
e=UnityPy.load(*[str(D/f) for f in ['globalgamemanagers.assets','resources.assets','sharedassets1.assets','level0','level1']]);e.typetree_generator=g
files={Path(f.name).name:f for f in e.files.values() if hasattr(f,'objects')}
idx=json.loads(Path('work/analysis/asset_index.json').read_text(encoding='utf8'))
rows=[];errors=[];odin=[];count=0
def walk(x,path):
 if isinstance(x,str) and re.search('[A-Za-z]',x):yield path,x
 elif isinstance(x,dict):
  for k,v in x.items():
   if k not in ['SerializedBytes','m_EditorClassIdentifier']:yield from walk(v,path+'.'+k)
 elif isinstance(x,list):
  if x and all(isinstance(i,int) for i in x):return
  for i,v in enumerate(x):yield from walk(v,f'{path}[{i}]')
for r in idx:
 if r.get('type')!='MonoBehaviour' or r['file'] not in files:continue
 if r.get('namespace','').split('.')[0] not in ['Gameplay','Actions','Events','Effects','Conditions','_Scripts','Audio'] and r.get('assembly')!='Assembly-CSharp':continue
 try:
  o=files[r['file']].objects[r['path_id']];t=o.read_typetree();count+=1
  for p,s in walk(t,''):
   rows.append({'file':r['file'],'oid':r['path_id'],'class':r.get('namespace','')+'.'+r.get('class',''),'asset':r['name'],'field':p,'value':s})
  sd=t.get('serializationData',{}).get('SerializedBytes')
  if sd:
   for z in parse_odin(bytes(sd)):
    if re.search('[A-Za-z]',z['value']):odin.append({'file':r['file'],'oid':r['path_id'],'asset':r['name'],**z})
  if r['path_id'] in [11218,11220] and r['file']=='sharedassets1.assets':
   (W/f'tree_{r["path_id"]}.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
 except Exception as exc:errors.append({'file':r['file'],'oid':r['path_id'],'error':str(exc)})
for n,v in [('typed_strings',rows),('odin_strings',odin),('parse_errors',errors)]:
 (W/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
print('objects',count,'strings',len(rows),'odin',len(odin),'errors',len(errors))
print('NESTED DISPLAY CANDIDATES')
for r in rows:
 if any(x in r['field'].lower() for x in ['dialog','text','description','title','nameoverride','displayname','tooltip','label','message']) and r['field']!='.m_Name':print(json.dumps(r,ensure_ascii=False))
print('RESOURCE ODIN')
for r in odin:
 if r['oid']==11220 and r['file']=='sharedassets1.assets':print(json.dumps(r,ensure_ascii=False))
