import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,r'C:\Users\USER\Documents\Codex\2026-10-13\e-steamlibrary-steamapps-common-slots-and\work\pydeps')
import UnityPy

source=Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo\StarHome_Data\sharedassets1.assets')
out=Path('work/roundtrip')
out.mkdir(exist_ok=True)
env=UnityPy.load(str(source)); old=env.file
before={o.path_id:(o.type_id,len(o.get_raw_data()),hashlib.sha256(o.get_raw_data()).hexdigest()) for o in old.objects.values()}
dest=out/source.name
dest.write_bytes(old.save())
fresh=UnityPy.load(str(dest));new=fresh.file
after={o.path_id:(o.type_id,len(o.get_raw_data()),hashlib.sha256(o.get_raw_data()).hexdigest()) for o in new.objects.values()}
ext=lambda f:[(x.path,x.temp_empty,x.type,str(x.guid)) for x in f.externals]
result={'status':'PASS' if before==after and ext(old)==ext(new) else 'FAIL',
        'scope':'offline no-op container serialization and reread only; not a translated or runtime-tested game',
        'file':str(source),'original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'rebuilt_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
        'original_bytes':source.stat().st_size,'rebuilt_bytes':dest.stat().st_size,
        'object_count':len(before),'all_object_path_ids_type_ids_sizes_payload_hashes_equal':before==after,
        'external_references_equal':ext(old)==ext(new),'native_launch':'NOT_RUN'}
Path('work/analysis/asset_roundtrip.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
