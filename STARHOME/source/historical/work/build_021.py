from read_typed import *
from odin_context import parse_odin
import copy,hashlib,struct,shutil,re,collections,datetime
W=Path('work/expanded_021');P=Path('outputs/STARHOME_Localization_0.2.1');EV=P/'evidence';EV.mkdir(parents=True,exist_ok=True)
S=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo')
B=Path('work/native_test_0.2.0/StarHome');D=Path('work/native_test_0.2.1/StarHome');D.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads(Path('work/analysis/original_manifest.json').read_text(encoding='utf8'))
for r in manifest:
 q=D/r['path'];q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists():shutil.copy2(B/r['path'],q)
for rel in ['StarHome_Data/sharedassets1.assets','StarHome_Data/il2cpp_data/Metadata/global-metadata.dat']:
 shutil.copy2(Path('work/full_localization/release_0.2.0')/Path(rel).name,D/rel)
g=MappedGenerator();g.install_managed_resolver()
def load(d):
 e=UnityPy.load(*[str(d/'StarHome_Data'/f) for f in ['globalgamemanagers.assets','resources.assets','sharedassets1.assets']]);e.typetree_generator=g
 return next(f for f in e.files.values() if f.name.endswith('sharedassets1.assets'))
a=load(D);beforehash={i:hashlib.sha256(o.get_raw_data()).hexdigest() for i,o in a.objects.items()}
changes=[];edited=set();expected={};noops=[]
def read(oid):
 o=a.objects[oid];raw=o.get_raw_data();t=o.read_typetree();o.save_typetree(t);assert o.get_raw_data()==raw,('no-op',oid);noops.append(oid);return t
def save(oid,t):a.objects[oid].save_typetree(t);edited.add(oid);expected[oid]=copy.deepcopy(t)
def row(oid,field,x,y):changes.append({'object':oid,'field':field,'source':x,'translation':y})
t=read(11218);old=copy.deepcopy(t);v=t['_firstBirthDialogue']
v['Title']='帕維爾・伊雷克'
v['Description']='好消息，指揮官！我們的人口增加了！在 FTL 航行期間，只要每個人都吃得飽，庫存中也有充足的食物，大家就能成家育兒。'
v['Options'][0]['OptionText']='確定'
for field in ['Title','Description']:row(11218,'_firstBirthDialogue.'+field,old['_firstBirthDialogue'][field],v[field])
row(11218,'_firstBirthDialogue.Options[0].OptionText','OK','確定')
z=copy.deepcopy(t);z['_firstBirthDialogue']=old['_firstBirthDialogue'];assert z==old;save(11218,t)
t=read(11217);old=copy.deepcopy(t)
for v,y in zip(t['<ThreatIcons>k__BackingField'],['可能有威脅','中度威脅','高度威脅','極高威脅']):
 row(11217,'ThreatIcons.Name',v['Name'],y);v['Name']=y
z=copy.deepcopy(t)
for x,y in zip(z['<ThreatIcons>k__BackingField'],old['<ThreatIcons>k__BackingField']):x['Name']=y['Name']
assert z==old;save(11217,t)
# Use the game's display-only override dictionary; enum names and all numeric IDs stay intact.
resources={0:'無',1:'食物',2:'水',3:'原料',4:'金屬',5:'電子零件',6:'化學品',7:'彈藥',8:'核彈',9:'燃料',10:'採礦船',11:'攻擊中隊',12:'人口',13:'廢棄物',14:'雷楚座標',15:'商品',16:'護衛艦',17:'研究資料'}
t=read(11220);old=copy.deepcopy(t);raw=bytes(t['serializationData']['SerializedBytes']);rs=parse_odin(raw)
values=[r for r in rs if r['field']=='$v' and r['nodes'] and r['nodes'][0]['name']=='_resourceNameOverrides'];assert [r['value'] for r in values]==['Raw Materials','Mining Ship','Attack Squadron']
start=values[0]['nodes'][-1]['offset'];end=values[-1]['value_end']+1
assert raw[start-9]==6 and struct.unpack_from('<q',raw,start-8)[0]==3 and raw[end-1]==5 and raw[end]==7
def os(x):
 b=x.encode('utf-16-le');return b'\x01'+struct.pack('<i',len(b)//2)+b
entries=b''.join(b'\x04\x2e\x1d'+os('$k')+struct.pack('<q',i)+b'\x27'+os('$v')+os(v)+b'\x05' for i,v in resources.items())
new=raw[:start-9]+b'\x06'+struct.pack('<q',len(resources))+entries+raw[end:]
after=parse_odin(new);assert [r['value'] for r in after if r['field']=='$v' and r['nodes'][0]['name']=='_resourceNameOverrides']==list(resources.values())
assert new[:start-9]==raw[:start-9] and new[start+len(entries):]==raw[end:]
t['serializationData']['SerializedBytes']=list(new);z=copy.deepcopy(t);z['serializationData']['SerializedBytes']=old['serializationData']['SerializedBytes'];assert z==old
save(11220,t)
for i,y in resources.items():row(11220,f'_resourceNameOverrides[{i}]',next((v['value'] for v in values if struct.unpack_from('<q',raw,v['value_start']-23)[0]==i),''),y)
# Translate remaining unambiguous prose even in original test/pool descriptions.
for oid,field,x,y in [(11242,'Description','zone click','點擊區域'),(11245,'_description','Middle','中間'),(11246,'_description','Middle','中間'),(11399,'<Description>k__BackingField','Burst the Flak Barrage zone fills its area with. Spawned by FlakBarrageZone, not by shells.','填滿防空彈幕區域的爆炸效果。由 FlakBarrageZone 產生，而非由砲彈產生。')]:
 t=read(oid);old=copy.deepcopy(t);raw=bytes(t['serializationData']['SerializedBytes']);rs=parse_odin(raw);matches=[r for r in rs if r['field']==field and r['value']==x];assert len(matches)==1,(oid,matches)
 r=matches[0];new=raw[:r['value_start']]+os(y)+raw[r['value_end']:];after=parse_odin(new)
 assert [(z['field'],z['value']) for z in after]==[(z['field'],y if z is r else z['value']) for z in rs]
 assert new[:r['value_start']]==raw[:r['value_start']] and new[r['value_start']+len(os(y)):]==raw[r['value_end']:]
 t['serializationData']['SerializedBytes']=list(new);z=copy.deepcopy(t);z['serializationData']=old['serializationData'];assert z==old
 row(oid,field,x,y);save(oid,t)
# One shared literal is used both as a visible heading and an element lookup.
# Rename that exact UXML query key in both serialized mirrors and matching USS selectors.
idx=json.loads(Path('work/analysis/asset_index.json').read_text(encoding='utf8'))
ui_renames=[];styles=[]
def replace_key(x,path=''):
 n=0
 if isinstance(x,dict):
  if x.get('name')=='name' and x.get('value')=='Construction':x['value']='建造';ui_renames.append(path+'.value');n+=1
  for k,v in x.items():
   if k=='name' and v=='Construction':x[k]='建造';ui_renames.append(path+'.name');n+=1
   elif isinstance(v,(dict,list)):n+=replace_key(v,path+'.'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):n+=replace_key(v,f'{path}[{i}]')
 return n
for rec in idx:
 if rec['file']!='sharedassets1.assets':continue
 oid=rec['path_id']
 if rec.get('class')=='VisualTreeAsset':
  t=a.objects[oid].read_typetree()
  if replace_key(t,str(oid)):
   read(oid);save(oid,t)
 elif rec.get('class')=='StyleSheet':
  t=a.objects[oid].read_typetree()
  def selector_scan(x,path=''):
   if isinstance(x,dict):
    for k,v in x.items():
     if isinstance(v,str) and (v=='Construction' or '#Construction' in v):styles.append({'object':oid,'field':path+'.'+k,'value':v})
     elif isinstance(v,(dict,list)):selector_scan(v,path+'.'+k)
   elif isinstance(x,list):
    for i,v in enumerate(x):selector_scan(v,f'{path}[{i}]')
  selector_scan(t)
assert len(ui_renames)==2,ui_renames
assert not styles,styles
target=D/'StarHome_Data/sharedassets1.assets';target.write_bytes(a.save());fresh=load(D)
assert set(fresh.objects)==set(a.objects)
for i in a.objects:
 if i not in edited:assert hashlib.sha256(fresh.objects[i].get_raw_data()).hexdigest()==beforehash[i],i
for i,t in expected.items():assert fresh.objects[i].read_typetree()==t,('reload',i)
# Append a new live string-literal pool while preserving every index and unrelated section.
meta=(D/'StarHome_Data/il2cpp_data/Metadata/global-metadata.dat').read_bytes();lo,ls,n=struct.unpack_from('<III',meta,8);do,ds,dc=struct.unpack_from('<III',meta,20)
offsets=list(struct.unpack_from(f'<{n}I',meta,lo))+[ds];old=[meta[do+offsets[i]:do+offsets[i+1]].decode('utf8') for i in range(n)]
lm={5465:'離開',10207:'準備完成',6036:'艦隊',10664:'略過',10891:'傳送',10211:'替換',10213:'重新開始',275:'與',2449:'套用',3440:'取消',4249:'關閉',4440:'建造',4451:'消耗',4827:'放棄變更',6302:'食物',9422:'關閉',13365:'未綁定',14184:'水',2930:'小行星 #{0}',4578:'護衛艦 #{0}',6190:'戰鬥機中隊 #{0}',7030:'人類太空站 #{0}',10251:'採礦船 #{0}',11296:'中隊 #{0}',14270:'殘骸 #{0}'}
new=[lm.get(i,x) for i,x in enumerate(old)];buf=bytearray(meta);pos=0;offs=[];chunks=[]
for s in new:offs.append(pos);z=s.encode('utf8');chunks.append(z);pos+=len(z)
newpos=(len(buf)+3)//4*4;buf.extend(bytes(newpos-len(buf)));buf.extend(b''.join(chunks));struct.pack_into(f'<{n}I',buf,lo,*offs);struct.pack_into('<III',buf,20,newpos,pos,dc)
assert n==21110 and sum(x!=y for x,y in zip(old,new))==len(lm)
assert all(x==y or 20<=i<32 or lo<=i<lo+n*4 for i,(x,y) in enumerate(zip(meta,buf)))
for i in lm:
 assert collections.Counter(re.findall(r'\{[^{}]+\}',old[i]))==collections.Counter(re.findall(r'\{[^{}]+\}',new[i]))
(D/'StarHome_Data/il2cpp_data/Metadata/global-metadata.dat').write_bytes(buf)
# Separate native-test identity, with original balance and input logic.
gg=UnityPy.load(str(S/'StarHome_Data/globalgamemanagers'));ps=next(o for o in gg.objects if o.type.name=='PlayerSettings');raw=ps.get_raw_data()
def packed(s):
 z=s.encode('utf8');z=struct.pack('<i',len(z))+z;return z+bytes((-len(z))%4)
for x,y in [('Digifox','MetiTests'),('StarHome','StarHome_ZH_021')]:assert raw.count(packed(x))==1;raw=raw.replace(packed(x),packed(y),1)
ps.set_raw_data(raw);(D/'StarHome_Data/globalgamemanagers').write_bytes(gg.file.save());(D/'StarHome_Data/app.info').write_text('MetiTests\nStarHome_ZH_021\n',encoding='utf8');(D/'steam_appid.txt').write_text('5314340',encoding='ascii')
result={'version':'0.2.1','built_at':datetime.datetime.now().astimezone().isoformat(),'changed_objects_vs_0_2_0':sorted(edited),'no_op_objects':noops,'resource_display_names':resources,'ui_query_key_mirrors':ui_renames,'style_key_dependencies':styles,'metadata_changes':[{'index':i,'source':old[i],'translation':new[i]} for i in lm],'validation':{'asset_reload':'PASS','untouched_objects':'PASS','resource_dictionary_complete_18_enum_values':'PASS','unrelated_resource_config_bytes':'PASS','population_balance_and_dialogue_options':'PASS','metadata_unselected_strings_and_sections':'PASS'},'user_entry_exit':'USER_REPORTED_PASS','historical_shutdown_crash':'Previous isolated test only; user reports normal entry and exit.','native_testing':'PENDING'}
for name,value in [('build.json',result),('additional_translations.json',changes)]: (EV/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
for rel in ['StarHome_Data/sharedassets1.assets','StarHome_Data/il2cpp_data/Metadata/global-metadata.dat']:
 q=P/'payload'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/rel,q)
print(json.dumps(result,ensure_ascii=False,indent=2))
