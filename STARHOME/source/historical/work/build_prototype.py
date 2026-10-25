from read_typed import *
import collections,copy,hashlib,re,struct

SRC=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo')
DST=Path('work/native_test/StarHome').resolve()
EV=Path('work/prototype_evidence')
DATA=SRC/'StarHome_Data'
g=MappedGenerator();g.install_managed_resolver()
env=UnityPy.load(str(DATA/'globalgamemanagers.assets'),str(DATA/'sharedassets1.assets'))
env.typetree_generator=g
asset=next(f for f in env.files.values() if f.name.endswith('sharedassets1.assets'))
original={i:hashlib.sha256(o.get_raw_data()).hexdigest() for i,o in asset.objects.items()}
changes=[];noop=[]
translations={r['source']:r['zh_Hant'] for r in json.loads(Path('outputs/STARHOME_Localization_Stage1/02_繁中試譯.json').read_text(encoding='utf8'))}
translations.update(json.loads(Path('work/prototype_extra_translations.json').read_text(encoding='utf8')))
translations.update(json.loads(Path('work/prototype_followup_translations.json').read_text(encoding='utf8')))
translations.update(json.loads(Path('work/prototype_tooltip_translations.json').read_text(encoding='utf8')))
ptr=lambda i:{'m_FileID':0,'m_PathID':i}

def checked(o):
    before=o.get_raw_data();t=o.read_typetree();o.save_typetree(t)
    assert o.get_raw_data()==before,('No-op mismatch',o.path_id)
    noop.append({'path_id':o.path_id,'bytes':len(before),'byte_identical':True})
    return t

def clone(source):
    base=asset.objects[source];new=copy.copy(base);new.path_id=max(asset.objects)+1
    new.data=base.get_raw_data();asset.objects[new.path_id]=new
    return new

def translated(src,where):
    if src not in translations:return src
    result=translations[src]
    assert collections.Counter(re.findall(r'\{[^{}]+\}',src))==collections.Counter(re.findall(r'\{[^{}]+\}',result))
    assert collections.Counter(re.findall(r'<[^>]+>',src))==collections.Counter(re.findall(r'<[^>]+>',result))
    changes.append({'where':where,'source':src,'translation':result})
    return result

# Add a dedicated dynamic TextCore fallback without replacing the Barlow fonts.
font_obj=clone(1451);font=checked(font_obj)
font['m_Name']='Meti TC Prototype Regular';font['m_FontNames']=['Meti TC Prototype']
font['m_FontData']=Path('work/prototype_evidence/MetiTCPrototype-Regular.ttf').read_bytes()
font_obj.save_typetree(font)
tex_obj=clone(1075);tex=checked(tex_obj);tex['m_Name']='Meti TC Prototype SDF Atlas';tex_obj.save_typetree(tex)
mat_obj=clone(207);mat=checked(mat_obj);mat['m_Name']='Meti TC Prototype SDF Material'
def rewrite_texture(value):
    if isinstance(value,dict):
        if value==ptr(1075):value['m_PathID']=tex_obj.path_id
        else:
            for v in value.values():rewrite_texture(v)
    elif isinstance(value,(list,tuple)):
        for v in value:rewrite_texture(v)
rewrite_texture(mat);mat_obj.save_typetree(mat)
fa_obj=clone(11150);fa=checked(fa_obj)
fa['m_Name']='Meti TC Prototype SDF';fa['m_Material']=ptr(mat_obj.path_id)
fa['m_SourceFontFile']=ptr(font_obj.path_id);fa['m_SourceFontFileGUID']=''
fa['m_SourceFontFilePath']='';fa['m_AtlasPopulationMode']=1
fa['m_AtlasTextures']=[ptr(tex_obj.path_id)];fa['m_FallbackFontAssetTable']=[]
fa['m_GlyphTable']=[];fa['m_CharacterTable']=[]
fa['m_FontFeatureTable']={k:[] for k in fa['m_FontFeatureTable']}
fi=json.loads((EV/'font_build.json').read_text(encoding='utf8'));point=fa['m_FaceInfo']['m_PointSize'];unit=fi['unitsPerEm']
face=fa['m_FaceInfo'];face['m_FamilyName']=fi['family'];face['m_StyleName']='Regular';face['m_FaceIndex']=0
face['m_UnitsPerEM']=unit;face['m_AscentLine']=point*fi['ascent']/unit;face['m_DescentLine']=point*fi['descent']/unit
face['m_LineHeight']=point*(fi['ascent']-fi['descent']+fi['lineGap'])/unit
face['m_CapLine']=point*fi['capHeight']/unit;face['m_MeanLine']=point*fi['xHeight']/unit
fa_obj.save_typetree(fa)
for i in range(11145,11154):
    o=asset.objects[i];t=checked(o)
    t['m_FallbackFontAssetTable'].append(ptr(fa_obj.path_id));o.save_typetree(t)

# Translate both UXML attribute values and their UxmlSerializedData counterparts.
ui_ids=[11765,11780,11785,11816]
for i in ui_ids:
    o=asset.objects[i];t=checked(o)
    for ref in t['references']['RefIds']:
        d=ref.get('data')
        if not d:continue
        for p in d.get('m_Properties',[]):
            if p['name'] in ['text','label','tooltip']:
                src=p['value'];p['value']=translated(src,f'UI:{i}:rid={ref["rid"]}:{p["name"]}')
                if i==11816 and src=='Continue':p['value']='繼續';changes[-1]['translation']='繼續'
        if 'UxmlSerializedData' in ref['type']['class']:
            for k in ['text','label','tooltip']:
                if isinstance(d.get(k),str):
                    src=d[k];d[k]=translated(src,f'UI:{i}:rid={ref["rid"]}:serialized.{k}')
                    if i==11816 and src=='Continue':d[k]='繼續';changes[-1]['translation']='繼續'
    o.save_typetree(t)

# Exact known fields of a starting construction module and sample research items.
for i in [11291,11412,11424,11427]:
    o=asset.objects[i];t=checked(o)
    for field in ['_name','_description','_techDescription']:
        if field in t:t[field]=translated(t[field],f'Data:{i}:{field}')
    o.save_typetree(t)

# Exact display fields only; difficulty enums, locks and balance remain byte-equal.
difficulty_ids=[11206,11207,11208,11209]
for i in difficulty_ids:
    o=asset.objects[i];t=checked(o);before=copy.deepcopy(t)
    for field in ['<Name>k__BackingField','<Description>k__BackingField']:
        t[field]=translated(t[field],f'Difficulty:{i}:{field}')
    assert {k:v for k,v in t.items() if k not in ['<Name>k__BackingField','<Description>k__BackingField']}=={k:v for k,v in before.items() if k not in ['<Name>k__BackingField','<Description>k__BackingField']}
    o.save_typetree(t)

def odin_string(b,p):
    if p+5>len(b) or b[p] not in [0,1]:return None
    w=b[p]+1;n=struct.unpack_from('<i',b,p+1)[0]
    if not 0<=n<=10000 or p+5+n*w>len(b):return None
    end=p+5+n*w
    s=b[p+5:end].decode('latin1' if w==1 else 'utf-16-le',errors='strict')
    return s,end

def patch_odin(payload,asset_id):
    edits=[]
    for m in re.finditer(b'\x27[\x00\x01]',payload):
        try:
            k=odin_string(payload,m.start()+1)
            if not k:continue
            name,pos=k
            if name not in ['Title','Description','OptionText','Text','_title','_text','BracketText','<Title>k__BackingField','<Description>k__BackingField','_description','Name']:continue
            val=odin_string(payload,pos)
            if not val:continue
            src,end=val
            if name=='Name' and (asset_id!=11243 or src not in {
                'Camera Movement','Zoom Out/In','Click On Task to get to the Asteroid','Reset Camera',
                'Select Flagship','Send Flagship To Destination','Fasten Game','Undock Ships','Select Miner Ships',
                'Mine Asteroid','How to Fight I.','Destroy projected enemies','Guard Capital Ship','Defend Capital Ship',
                'Investigate Threat','Search Wreck','Salvage Wreck','How to Fight II.','Select Ship','Collect Debris',
                'Collect Ammo','Launch Nuke','Travel to Your Colony','Destroy Asteroid'}):continue
            zh=translated(src,f'Odin:{asset_id}:{m.start()}:{name}')
            if name=='OptionText' and src=='Continue':zh='繼續';changes[-1]['translation']=zh
            if zh==src:continue
            encoded=zh.encode('utf-16-le');rep=b'\x01'+struct.pack('<i',len(encoded)//2)+encoded
            edits.append((pos,end,rep,src,zh,name))
        except (UnicodeError,ValueError):continue
    result=payload
    for a,b,rep,*_ in reversed(edits):result=result[:a]+rep+result[b:]
    assert all(edits[i][1]<=edits[i+1][0] for i in range(len(edits)-1))
    return result,len(edits)

odin_counts=[]
for i in [11228,11243]:
    o=asset.objects[i];t=checked(o);serial=t['serializationData']
    old=bytes(serial['SerializedBytes']);new,n=patch_odin(old,i)
    serial['SerializedBytes']=list(new)
    o.save_typetree(t);odin_counts.append({'path_id':i,'translated_records':n,'old_payload':len(old),'new_payload':len(new)})

destination=DST/'StarHome_Data/sharedassets1.assets'
destination.write_bytes(asset.save())
fresh=UnityPy.load(str(DATA/'globalgamemanagers.assets'),str(destination));fresh.typetree_generator=g
newasset=next(f for f in fresh.files.values() if f.name.endswith('sharedassets1.assets'))
modified=[i for i,h in original.items() if hashlib.sha256(newasset.objects[i].get_raw_data()).hexdigest()!=h]
expected=set(range(11145,11154))|set(ui_ids)|set(difficulty_ids)|{11291,11412,11424,11427,11228,11243}
assert set(modified)==expected,(modified,expected)
assert len(newasset.objects)==len(original)+4
for i in expected|{font_obj.path_id,tex_obj.path_id,mat_obj.path_id,fa_obj.path_id}:
    newasset.objects[i].read_typetree()

# Preserve literal indices. Relocate only the string data section to appended bytes.
meta_path=DATA/'il2cpp_data/Metadata/global-metadata.dat';meta=bytearray(meta_path.read_bytes())
lo,ls,count=struct.unpack_from('<III',meta,8);data_off,data_len,data_count=struct.unpack_from('<III',meta,20)
offsets=list(struct.unpack_from(f'<{count}I',meta,lo))+[data_len]
allowed=['Start Game','YES','NO','Do you really want to exit game and return to Windows?','Press "','" to activate.','New Game','Do you really want to start a new game ?','PLAY TUTORIAL','Skip Tutorial','You have already finished the tutorial. Skip it and start with bonus resources?','Save Game','Load Game','Exit to Desktop','You Survived: {0} Days']
chunks=[];new_offsets=[];literal_edits=[];current=0
for i in range(count):
    raw=bytes(meta[data_off+offsets[i]:data_off+offsets[i+1]])
    src=raw.decode('utf8')
    if src in allowed and src in translations:
        zh=translated(src,f'Literal:{i}');raw=zh.encode('utf8');literal_edits.append({'index':i,'source':src,'translation':zh})
    chunks.append(raw);new_offsets.append(current);current+=len(raw)
new_data=b''.join(chunks);new_pos=(len(meta)+3)//4*4
meta.extend(bytes(new_pos-len(meta)));meta.extend(new_data)
struct.pack_into(f'<{count}I',meta,lo,*new_offsets);struct.pack_into('<III',meta,20,new_pos,len(new_data),data_count)
(DST/'StarHome_Data/il2cpp_data/Metadata/global-metadata.dat').write_bytes(meta)
assert count==21110
for i,raw in enumerate(chunks):
    src=meta_path.read_bytes()[data_off+offsets[i]:data_off+offsets[i+1]] if False else None
    assert new_data[new_offsets[i]:new_offsets[i+1] if i+1<count else len(new_data)]==raw

# Change the test copy's Unity identity to isolate persistent data and PlayerPrefs.
gg=UnityPy.load(str(DATA/'globalgamemanagers'));ps=next(o for o in gg.objects if o.type.name=='PlayerSettings')
raw=ps.get_raw_data()
def packed(s):
    b=s.encode('utf8');data=struct.pack('<i',len(b))+b;return data+bytes((-len(data))%4)
for old,new in [('Digifox','MetiTests'),('StarHome','StarHome_ZH_Prototype_001')]:
    needle=packed(old);assert raw.count(needle)==1,(old,raw.count(needle));raw=raw.replace(needle,packed(new),1)
ps.set_raw_data(raw);(DST/'StarHome_Data/globalgamemanagers').write_bytes(gg.file.save())
(DST/'StarHome_Data/app.info').write_text('MetiTests\nStarHome_ZH_Prototype_001\n',encoding='utf8')

result={'prototype':'Meti STARHOME zh-Hant 0.1.2 isolated sample','game_version':'0.4.7b','root':str(DST),
        'identity':{'company':'MetiTests','product':'StarHome_ZH_Prototype_001'},
        'expected_persistent_data':r'C:\Users\USER\AppData\LocalLow\MetiTests\StarHome_ZH_Prototype_001',
        'existing_object_changes':modified,'added_object_ids':[font_obj.path_id,tex_obj.path_id,mat_obj.path_id,fa_obj.path_id],
        'source_font_object':font_obj.path_id,'fallback_font_asset_object':fa_obj.path_id,
        'translation_occurrences':len(changes),'unique_source_strings':len(set(x['source'] for x in changes)),
        'odin':odin_counts,'literal_changes':literal_edits,'no_op_validated_objects':noop,
        'container_reload':'PASS','untouched_object_payloads':'PASS','native_test':'PENDING',
        'changed_relative_files':['StarHome_Data/sharedassets1.assets','StarHome_Data/il2cpp_data/Metadata/global-metadata.dat','StarHome_Data/globalgamemanagers','StarHome_Data/app.info']}
(EV/'prototype_build.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
(EV/'prototype_translations.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ['no_op_validated_objects','literal_changes']},ensure_ascii=False,indent=2))
