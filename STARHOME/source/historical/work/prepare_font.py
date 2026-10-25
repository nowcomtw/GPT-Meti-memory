from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('work/pydeps').resolve()))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
font=TTFont(r'C:\Windows\Fonts\NotoSansTC-VF.ttf')
font=instantiateVariableFont(font,{'wght':400},inplace=True,updateFontNames=True)
names={1:'Meti TC Prototype',2:'Regular',3:'Meti TC Prototype Regular 001',4:'Meti TC Prototype Regular',6:'MetiTCPrototype-Regular',16:'Meti TC Prototype',17:'Regular'}
for rec in font['name'].names:
    if rec.nameID in names:
        try:rec.string=names[rec.nameID].encode(rec.getEncoding())
        except Exception:pass
out=Path('work/prototype_evidence/MetiTCPrototype-Regular.ttf')
font.save(out)
assert 'fvar' not in font
cmap=font.getBestCmap()
test='繁體中文漢化研究艦隊歡迎指揮官懷亞特'
assert all(ord(c) in cmap for c in test)
info={'source':r'C:\Windows\Fonts\NotoSansTC-VF.ttf','weight':400,'output':str(out.resolve()),'bytes':out.stat().st_size,'family':font['name'].getBestFamilyName(),'sample':test,'all_sample_glyphs_present':True,'unitsPerEm':font['head'].unitsPerEm,'ascent':font['hhea'].ascent,'descent':font['hhea'].descent,'lineGap':font['hhea'].lineGap,'capHeight':font['OS/2'].sCapHeight,'xHeight':font['OS/2'].sxHeight}
Path('work/prototype_evidence/font_build.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(info,ensure_ascii=True))
