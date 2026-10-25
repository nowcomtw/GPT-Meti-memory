import struct
def parse_odin(raw):
 p=0;stack=[];types={};rows=[]
 def num(fmt):
  nonlocal p
  n=struct.unpack_from(fmt,raw,p)[0];p+=struct.calcsize(fmt);return n
 def string():
  nonlocal p
  w=num('<B')+1;assert w in (1,2);n=num('<i');assert 0<=n<1000000
  z=raw[p:p+n*w];assert len(z)==n*w;p+=n*w;return z.decode('latin1' if w==1 else 'utf-16-le')
 def typ():
  tag=num('<B')
  if tag==0x2e:return None
  i=num('<i')
  if tag==0x2f:types[i]=string()
  else:assert tag==0x30,(p,tag)
  return types[i]
 widths={**{k:1 for k in [15,16,17,18,43,44]},**{k:2 for k in [19,20,21,22,37,38]},**{k:4 for k in [9,10,11,12,23,24,25,26,31,32]},**{k:8 for k in [27,28,29,30,33,34]},**{k:16 for k in [13,14,35,36,41,42]}}
 named={1,3,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,50}
 while p<len(raw):
  pos=p;tag=num('<B');name=string() if tag in named else None
  if tag in (1,2,3,4):
   t=typ();ref=num('<i') if tag in (1,2) else None
   stack.append({'name':name,'type':t,'ref':ref,'offset':pos})
  elif tag==5:assert stack,(p,'stack empty');stack.pop()
  elif tag==6:num('<q')
  elif tag==7:pass
  elif tag==8:
   n=num('<i');w=num('<i');assert n>=0 and w in (1,2,4,8,16);p+=n*w
  elif tag in (39,40,50,51):
   start=p;v=string();rows.append({'field':name,'value':v,'offset':pos,'value_start':start,'value_end':p,'nodes':[dict(x) for x in stack]})
  elif tag in widths:p+=widths[tag]
  elif tag in (45,46):pass
  elif tag==49:break
  else:raise ValueError((pos,'unknown entry',tag))
 assert p==len(raw),(p,len(raw));assert not stack,(p,'unclosed nodes',len(stack))
 return rows

if __name__=='__main__':
 from read_typed import *
 import collections,re
 g=MappedGenerator();g.install_managed_resolver();d=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo\StarHome_Data');e=UnityPy.load(str(d/'globalgamemanagers.assets'),str(d/'sharedassets1.assets'));e.typetree_generator=g;a=next(f for f in e.files.values() if f.name.endswith('sharedassets1.assets'))
 out=[];errors=[]
 for oid in [11215,11231,11232,11235,11237,11238,11239,11243,11244,11245,11246,11247]:
  try:
   t=a.objects[oid].read_typetree();rs=parse_odin(bytes(t['serializationData']['SerializedBytes']))
   for r in rs:
    if r['field']=='Name':out.append({'path_id':oid,'asset':t['m_Name'],**r})
  except Exception as exc:errors.append({'path_id':oid,'error':str(exc)})
 Path('work/full_localization/odin_name_contexts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print('ERRORS',errors)
 headers=[r for r in out if len(r['nodes'])>=2 and (r['nodes'][-2]['type'] or '').startswith('Actions.Section,')]
 Path('work/full_localization/section_names.json').write_text(json.dumps(headers,ensure_ascii=False,indent=2),encoding='utf8')
 print('HEADERS',len(headers));print('\n'.join(f"{r['path_id']} | {r['offset']} | {r['value']}" for r in headers))
