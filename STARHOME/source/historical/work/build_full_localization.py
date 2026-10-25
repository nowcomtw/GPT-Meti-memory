from read_typed import *
from odin_context import parse_odin
import collections,copy,hashlib,re,struct,shutil,datetime
SRC=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo')
DST=Path('work/native_test_0.2.0/StarHome').resolve()
BASE=Path('outputs/STARHOME_Localization_0.1.2')
OUT=Path('outputs/STARHOME_Localization_0.2.0');EV=OUT/'evidence';EV.mkdir(parents=True,exist_ok=True)
W=Path('work/full_localization');AUD=Path('outputs/STARHOME_Localization_Coverage_Audit_2026-10-21')
trans=json.loads((W/'translations.json').read_text(encoding='utf8'))
section_titles=json.loads((W/'section_titles.json').read_text(encoding='utf8'))
validation=json.loads((W/'translation_validation.json').read_text(encoding='utf8'));assert not validation['missing'] and not validation['issues']
manifest=json.loads(Path('work/analysis/original_manifest.json').read_text(encoding='utf8'))
if not DST.exists():
 DST.mkdir(parents=True)
 for r in manifest:
  p=SRC/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
  q=DST/r['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
else:
 assert not any(p.suffix=='.lock' for p in DST.rglob('*'))
g=MappedGenerator();g.install_managed_resolver()
def load_asset(path):
 root=path.parent
 e=UnityPy.load(str(root/'globalgamemanagers.assets'),str(root/'resources.assets'),str(path));e.typetree_generator=g
 return next(f for f in e.files.values() if f.name.endswith('sharedassets1.assets'))
a=load_asset(SRC/'StarHome_Data/sharedassets1.assets')
shutil.copy2(BASE/'payload/StarHome_Data/sharedassets1.assets',DST/'StarHome_Data/sharedassets1.assets')
b=load_asset(DST/'StarHome_Data/sharedassets1.assets')
basehash={i:hashlib.sha256(o.get_raw_data()).hexdigest() for i,o in b.objects.items()}
originalhash={i:hashlib.sha256(o.get_raw_data()).hexdigest() for i,o in a.objects.items()}
changes=[];noops=[];excluded=[];handled=set();names=set();structures=[]
UI_FIELDS={'text':'text','label':'label','tooltip':'tooltip','title':'title','placeholder-text':'placeholderText','value':'value'}
DISPLAY={'Title','Description','OptionText','Text','_title','_text','BracketText','<Title>k__BackingField','<Description>k__BackingField','<EmptyDescription>k__BackingField','<Name>k__BackingField','_description'}
TOP={'_name','_description','_techDescription','<Name>k__BackingField','<Title>k__BackingField','<Description>k__BackingField','<EmptyDescription>k__BackingField','Text','Title','Description','OptionText','BracketText'}
def check_text(x,y,where):
 for pat in [r'\{[^{}]+\}',r'<[^>]+>',r'\d+(?:\.\d+)?%?']:
  assert collections.Counter(re.findall(pat,x))==collections.Counter(re.findall(pat,y)),(where,pat,x,y)
def translate(x,where):
 y=trans.get(x,x)
 if x!=y:check_text(x,y,where);changes.append({'where':where,'source':x,'translation':y})
 return y
def checked(oid):
 o=b.objects[oid];raw=o.get_raw_data()
 try:
  t=o.read_typetree();o.save_typetree(t)
  assert o.get_raw_data()==raw,'byte-identical no-op failed'
 except Exception as exc:
  o.set_raw_data(raw);excluded.append({'object':oid,'reason':'NO_OP_OR_PARSE_FAILURE','detail':str(exc)});return None
 noops.append({'object':oid,'bytes':len(raw),'status':'BYTE_IDENTICAL'});return t
def strip_ui(t):
 t=copy.deepcopy(t)
 for r in t['references']['RefIds']:
  d=r.get('data',{})
  for p in d.get('m_Properties',[]):
   if p['name'] in UI_FIELDS:p['value']=None
  if 'UxmlSerializedData' in r.get('type',{}).get('class',''):
   for k in UI_FIELDS.values():
    if isinstance(d.get(k),str):d[k]=None
 return t
def odin_strings(raw):
 def string(p):
  if p+5>len(raw) or raw[p] not in (0,1):return None
  w=raw[p]+1;n=struct.unpack_from('<i',raw,p+1)[0]
  if not 0<=n<=10000 or p+5+w*n>len(raw):return None
  end=p+5+w*n;s=raw[p+5:end].decode('latin1' if w==1 else 'utf-16-le')
  if any(ord(c)<32 and c not in '\r\n\t' for c in s):return None
  return s,end
 result=[]
 for m in re.finditer(b'\x27[\x00\x01]',raw):
  try:
   k=string(m.start()+1)
   if not k or not re.fullmatch(r'[A-Za-z_<>][A-Za-z0-9_<>+.`$\-]{0,120}',k[0]):continue
   v=string(k[1])
   if v:result.append({'field':k[0],'value':v[0],'offset':m.start(),'value_start':k[1],'value_end':v[1]})
  except UnicodeError:pass
 return result
def patch_odin(raw,oid):
 rows=odin_strings(raw);edits=[]
 section_positions=set()
 if 11231<=oid<=11249:
  for r in parse_odin(raw):
   if r['field']=='Name' and len(r['nodes'])>=2 and (r['nodes'][-2]['type'] or '').startswith('Actions.Section,') and r['value'] in section_titles:section_positions.add(r['offset'])
 for r in rows:
  section_name=r['offset'] in section_positions
  if r['field'] not in DISPLAY and not section_name:continue
  x=r['value']
  if section_name:
   y=section_titles[x];check_text(x,y,(oid,r['offset']));changes.append({'where':f'OdinSectionTitle:{oid}:{r["offset"]}:Name','source':x,'translation':y})
  else:y=translate(x,f'Odin:{oid}:{r["offset"]}:{r["field"]}')
  if x!=y:
   enc=y.encode('utf-16-le');edits.append((r['value_start'],r['value_end'],b'\x01'+struct.pack('<i',len(enc)//2)+enc))
 result=raw
 for start,end,rep in reversed(edits):result=result[:start]+rep+result[end:]
 after=odin_strings(result);assert len(rows)==len(after)
 for x,y in zip(rows,after):
  assert x['field']==y['field']
  if x['field'] not in DISPLAY and x['offset'] not in section_positions:assert x['value']==y['value'],('protected Odin',oid,x)
  check_text(x['value'],y['value'],(oid,x['offset']))
 guid=lambda z:collections.Counter(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',z.decode('latin1')))
 # Separate 8/16-bit records avoid relying on raw UTF-16 layout for GUID checks.
 refs=lambda rs:collections.Counter(v for r in rs for v in re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',r['value']))
 assert refs(rows)==refs(after)
 return result,len(edits)
audited=json.loads((AUD/'audited_objects.json').read_text(encoding='utf8'))
for rec in audited:
 if rec['file']!='sharedassets1.assets' or rec['class'] in ['TMPro.TextMeshProUGUI','UnityEngine.UI.Text']:continue
 oid=rec['path_id'];t=checked(oid)
 if t is None:continue
 before=copy.deepcopy(t);n0=len(changes)
 if rec['class']=='UnityEngine.UIElements.VisualTreeAsset':
  for r in t['references']['RefIds']:
   d=r.get('data',{})
   for p in d.get('m_Properties',[]):
    if p['name'] in ['name','class']:names.add(p['value'])
    if p['name'] in UI_FIELDS:p['value']=translate(p['value'],f'UI:{oid}:rid={r["rid"]}:{p["name"]}')
   if 'UxmlSerializedData' in r.get('type',{}).get('class',''):
    if isinstance(d.get('name'),str) and d['name']:names.add(d['name'])
    for k in UI_FIELDS.values():
     if isinstance(d.get(k),str):d[k]=translate(d[k],f'UI:{oid}:rid={r["rid"]}:serialized.{k}')
  assert strip_ui(before)==strip_ui(t),('UI structure',oid)
 else:
  for k in TOP:
   if isinstance(t.get(k),str):t[k]=translate(t[k],f'Data:{oid}:{k}')
  if rec['class']=='Gameplay.ShipsConfigData':
   for k in ['_shipNameFirstWords','_shipNameSecondWords']:
    t[k]=[translate(v,f'Data:{oid}:{k}[{j}]') for j,v in enumerate(t[k])]
  allowed=set(TOP)|({'_shipNameFirstWords','_shipNameSecondWords'} if rec['class']=='Gameplay.ShipsConfigData' else set())
  if isinstance(t.get('serializationData'),dict):
   sd=t['serializationData'];old=bytes(sd['SerializedBytes']);new,count=patch_odin(old,oid)
   if count:sd['SerializedBytes']=list(new)
   assert {k:v for k,v in before['serializationData'].items() if k!='SerializedBytes'}=={k:v for k,v in sd.items() if k!='SerializedBytes'},('Odin reference tables',oid)
   allowed.add('serializationData')
  assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in t.items() if k not in allowed},('data nontext structure',oid)
 if len(changes)>n0:
  b.objects[oid].save_typetree(t);handled.add(oid);structures.append({'object':oid,'class':rec['class'],'nontext_structure':'UNCHANGED'})
 print('.',end='',flush=True) if oid%40==0 else None
print('\nText objects changed beyond 0.1.2',len(handled),flush=True)
target=DST/'StarHome_Data/sharedassets1.assets';target.write_bytes(b.save())
fresh=load_asset(target)
assert set(fresh.objects)==set(b.objects)
assert all(hashlib.sha256(fresh.objects[i].get_raw_data()).hexdigest()==basehash[i] for i in basehash if i not in handled)
for i in handled:fresh.objects[i].read_typetree()
changed_vs_original=[i for i,h in originalhash.items() if hashlib.sha256(fresh.objects[i].get_raw_data()).hexdigest()!=h]
# Metadata allow list is independent of the asset dictionary. Never apply a global
# source-string replacement to runtime literals that could also be query keys.
meta=(SRC/'StarHome_Data/il2cpp_data/Metadata/global-metadata.dat').read_bytes()
lo,ls,n=struct.unpack_from('<III',meta,8);do,ds,dc=struct.unpack_from('<III',meta,20)
off=list(struct.unpack_from(f'<{n}I',meta,lo))+[ds]
old=[meta[do+off[i]:do+off[i+1]].decode('utf8') for i in range(n)]
lm={r['index']:r['translation'] for r in json.loads((BASE/'evidence/prototype_build.json').read_text(encoding='utf8'))['literal_changes']}
requested={int(k):v for k,v in json.loads((W/'metadata_zh.json').read_text(encoding='utf8')).items()}
refs=json.loads((W/'game_literal_references.json').read_text(encoding='utf8'))
for i,y in requested.items():
 assert any(r['literal_index']==i and r['text']==old[i] for r in refs),(i,'missing native use evidence')
 if old[i] in names:
  excluded.append({'literal_index':i,'source':old[i],'reason':'SHARED_WITH_UXML_ELEMENT_NAME','detail':'retain literal to preserve UI query keys'});continue
 check_text(old[i],y,f'Literal:{i}');lm[i]=y
new=[lm.get(i,x) for i,x in enumerate(old)];buf=bytearray(meta);chunks=[x.encode('utf8') for x in new]
offsets=[];pos=0
for c in chunks:offsets.append(pos);pos+=len(c)
data=b''.join(chunks);newpos=(len(buf)+3)//4*4;buf.extend(bytes(newpos-len(buf)));buf.extend(data)
struct.pack_into(f'<{n}I',buf,lo,*offsets);struct.pack_into('<III',buf,20,newpos,len(data),dc)
(DST/'StarHome_Data/il2cpp_data/Metadata/global-metadata.dat').write_bytes(buf)
assert n==21110 and {i for i,(x,y) in enumerate(zip(old,new)) if x!=y}==set(lm)
assert all(x==y or 20<=i<32 or lo<=i<lo+n*4 for i,(x,y) in enumerate(zip(meta,buf)))
literal_changes=[{'index':i,'source':old[i],'translation':new[i],'native_methods':sorted(set(r['method'] for r in refs if r['literal_index']==i))} for i in sorted(lm)]
# New isolated user-data identity, starting from unmodified PlayerSettings.
gg=UnityPy.load(str(SRC/'StarHome_Data/globalgamemanagers'));ps=next(o for o in gg.objects if o.type.name=='PlayerSettings');raw=ps.get_raw_data()
def packed(x):
 z=x.encode('utf8');z=struct.pack('<i',len(z))+z;return z+bytes((-len(z))%4)
for x,y in [('Digifox','MetiTests'),('StarHome','StarHome_ZH_020')]:
 assert raw.count(packed(x))==1;raw=raw.replace(packed(x),packed(y),1)
ps.set_raw_data(raw);(DST/'StarHome_Data/globalgamemanagers').write_bytes(gg.file.save())
(DST/'StarHome_Data/app.info').write_text('MetiTests\nStarHome_ZH_020\n',encoding='utf8')
(DST/'steam_appid.txt').write_text('5314340',encoding='ascii')
result={'version':'0.2.0','game_version':'0.4.7b','built_at':datetime.datetime.now().astimezone().isoformat(),'source':str(SRC),'test_root':str(DST),'identity':{'company':'MetiTests','product':'StarHome_ZH_020'},'added_ids':sorted(set(fresh.objects)-set(a.objects)),'changed_existing_objects_vs_original':changed_vs_original,'additional_text_objects_vs_0_1_2':sorted(handled),'additional_asset_translation_occurrences':len(changes),'metadata_literal_changes':len(literal_changes),'excluded':excluded,'no_op_failures':sum(r['reason']=='NO_OP_OR_PARSE_FAILURE' for r in excluded),'container_reload':'PASS','untouched_objects_vs_base':'PASS','ui_structure':'PASS_UNCHANGED','data_nontext_structure':'PASS_UNCHANGED','odin_protected_strings_and_guid_references':'PASS_UNCHANGED','metadata_unselected_literals_and_sections':'PASS_UNCHANGED','native_test':'PENDING'}
for name,value in [('build.json',result),('additional_asset_translations.json',changes),('literal_changes.json',literal_changes),('no_op_validation.json',noops),('structure_validation.json',structures)]:
 (EV/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copy2(W/'translations.json',EV/'translations.json');shutil.copy2(W/'exceptions.json',EV/'translation_exceptions.json')
print(json.dumps(result,ensure_ascii=False,indent=2))
