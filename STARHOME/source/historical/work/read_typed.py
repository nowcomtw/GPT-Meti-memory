import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf8')
sys.path.insert(0,r'C:\Users\USER\Documents\Codex\2026-10-13\e-steamlibrary-steamapps-common-slots-and\work\pydeps')
import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
from UnityPy.helpers import TypeTreeHelper

class MappedGenerator(TypeTreeGenerator):
    def __init__(self):
        super().__init__('6000.3.15f1')
        self.mapping={r['name']:r.get('assembly','') for r in json.loads(Path('work/prototype_evidence/type_assembly_map.json').read_text())}
        self.load_local_dll_folder(str(Path('work/prototype_evidence/dummy_dll').resolve()))
    def get_nodes_up(self,assembly,fullname):
        actual=self.mapping.get(fullname,assembly)
        key=(actual,fullname)
        if key not in self.cache:
            raw=self.get_nodes(actual if actual.endswith('.dll') else actual+'.dll',fullname.replace('+','/'))
            for n in raw:
                if n.m_Level==1 and n.m_Name=='m_Enabled':n.m_MetaFlag |= 16384
            node=TypeTreeNode.from_list([TypeTreeNode(n.m_Level,n.m_Type,n.m_Name,0,0,m_MetaFlag=n.m_MetaFlag) for n in raw])
            def normalize(n):
                children=[normalize(c) for c in n.m_Children]
                typ=n.m_Type
                if typ.startswith('LazyLoadReference'):
                    typ='PPtr<$Object>'
                    children=[TypeTreeNode(n.m_Level+1,'int','m_FileID',4,0),TypeTreeNode(n.m_Level+1,'SInt64','m_PathID',8,0)]
                if children and children[0].m_Type=='Array' and typ in TypeTreeHelper.FUNCTION_READ_MAP:
                    data=children[0].m_Children[1]
                    if not (typ=='string' and data.m_Type=='char'):
                        typ='vector'
                return TypeTreeNode(n.m_Level,typ,n.m_Name,n.m_ByteSize,n.m_Version,m_Children=children,m_MetaFlag=n.m_MetaFlag)
            node=normalize(node)
            children=list(node.m_Children)
            # Unity 6000.3 UxmlAsset has an abstract SerializeReference parent;
            # the older generator omits it. Confirmed in Unity's UxmlObjectAsset.cs.
            if fullname in ['UnityEngine.UIElements.VisualElementAsset','UnityEngine.UIElements.TemplateAsset','UnityEngine.UIElements.UxmlObjectAsset','UnityEngine.UIElements.UxmlAsset'] and not any(c.m_Name=='m_Parent' for c in children):
                at=next(i for i,c in enumerate(children) if c.m_Name=='m_Id')+1
                children.insert(at,TypeTreeNode(1,'managedReference','m_Parent',8,0,m_Children=[TypeTreeNode(2,'SInt64','rid',8,0)]))
                node.m_Children=children
            self.cache[key]=node
        return self.cache[key]
    def install_managed_resolver(self):
        TypeTreeHelper.read_typetree_boost=None
        def resolve(ref,assetfile):
            typ=ref['type'];cls=typ['class'];ns=typ['ns'];asm=typ['asm']
            if not cls:return None
            fullname=(ns+'.' if ns else '')+cls.replace('/','+')
            node=self.get_nodes_up(asm,fullname)
            children=node.m_Children
            if len(children)>=4 and children[0].m_Name=='m_GameObject':
                managed=TypeTreeNode(0,node.m_Type,'Base',0,0,m_Children=children[4:])
                return managed
            return node
        TypeTreeHelper.get_ref_type_node=resolve
        original_write=TypeTreeHelper.write_value
        def write(value,node,writer,config):
            if node.m_Type=='ReferencedObject' and value['type']['class']=='':
                for child in node.m_Children:
                    if child.m_Type!='ReferencedObjectData':
                        write(value[child.m_Name],child,writer,config)
                if (node.m_MetaFlag or 0)&16384:writer.align_stream()
                return
            return original_write(value,node,writer,config)
        TypeTreeHelper.write_value=write

if __name__=='__main__':
    g=MappedGenerator()
    g.install_managed_resolver()
    r=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo\StarHome_Data')
    e=UnityPy.load(str(r/'globalgamemanagers.assets'),str(r/'sharedassets1.assets'))
    e.typetree_generator=g
    rows=[]
    for o in e.objects:
        if Path(o.assets_file.name).name!='sharedassets1.assets' or o.path_id not in [11150,11154,11231,11785,11765,11500]:continue
        try:
            t=o.read_typetree()
            Path(f'work/prototype_evidence/tree_{o.path_id}.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
            rows.append({'path_id':o.path_id,'status':'PASS_EXACT_READ','keys':list(t)})
        except Exception as exc:
            rows.append({'path_id':o.path_id,'status':'FAIL','error':str(exc)})
    print(json.dumps(rows,ensure_ascii=False,indent=2))
    Path('work/prototype_evidence/typed_read_status.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
