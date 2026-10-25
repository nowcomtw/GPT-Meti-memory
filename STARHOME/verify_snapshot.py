from pathlib import Path
import hashlib,json,collections,sys

def main():
    root=Path(__file__).resolve().parent
    rows=json.loads((root/'CHECKSUMS.json').read_text(encoding='utf8'))
    for row in rows:
        p=(root/row['path']).resolve()
        if not p.is_relative_to(root):raise ValueError('Path outside snapshot')
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('Hash mismatch: '+row['path'])
        if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['git_blob_sha1']:raise ValueError('Git blob mismatch: '+row['path'])
    ix=json.loads((root/'translations/index.json').read_text(encoding='utf8'))
    def read_parts(key):
        return [r for name in ix[key] for r in json.loads((root/name).read_text(encoding='utf8'))]
    catalog=read_parts('catalog_files');gloss=read_parts('glossary_files');literals=read_parts('runtime_literal_files')
    assert len(catalog)==ix['catalog_rows']
    assert len(gloss)==ix['glossary_entries'] and len({r['source'] for r in gloss})==len(gloss)
    ids=[r['index'] for r in literals]
    assert len(ids)==ix['final_runtime_literal_entries']==len(set(ids))==212
    assert all(0<=i<21110 for i in ids)
    assert len(json.loads((root/'translations/resource_names.json').read_text(encoding='utf8')))==18
    print('PASS:',len(rows),'files;',len(catalog),'catalog rows;',len(gloss),'glossary entries;',len(ids),'runtime literals')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print('FAIL:',str(exc),file=sys.stderr);sys.exit(1)
