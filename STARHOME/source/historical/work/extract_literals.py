import json
from pathlib import Path
import struct

path = Path(r'D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo\StarHome_Data\il2cpp_data\Metadata\global-metadata.dat')
b = path.read_bytes()
assert struct.unpack_from('<II', b) == (0xFAB11BAF, 39)
offset, size, count = struct.unpack_from('<III', b, 8)
base, data_size, _ = struct.unpack_from('<III', b, 20)
assert size == count * 4
offsets = list(struct.unpack_from(f'<{count}I', b, offset)) + [data_size]
assert all(0 <= x <= data_size for x in offsets)
assert offsets == sorted(offsets)
rows = []
for i in range(count):
    start, end = offsets[i:i+2]
    raw = b[base+start:base+end]
    rows.append({'index': i, 'file_offset':base+start,'byte_length':end-start,
                 'text':raw.decode('utf-8',errors='strict')})
out = Path(__file__).parent / 'analysis' / 'metadata_literals.json'
out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print('Extracted', len(rows), 'literals;', out.stat().st_size, 'output bytes')
for row in [r for r in rows if any(x in r['text'].lower() for x in ['new game','tutorial','language','food production','surviv','welcome'])][:30]:
    print(json.dumps(row, ensure_ascii=False))
