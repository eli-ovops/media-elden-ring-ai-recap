from pathlib import Path
import json,shutil,subprocess,hashlib,concurrent.futures
R=Path(__file__).resolve().parent; C=R.parent;pub=R/'public';source=C/'03-口播接收/原片'
clips=[('talk-1.mp4','9d4b1a182e0f0074ff92bacbe2bbdc82_raw.mp4',.233333333333,28.466666666667),('talk-2.mp4','ad772cd8d8dcac13349c4b5b0adcfed8_raw.mp4',.233333333333,42.6),('talk-3.mp4','9a00fbddfbe4a52eb4e8e26fff93833d_raw.mp4',.55,32.95)]
def make(x):
 name,src,start,dur=x;dest=pub/name
 if not dest.exists(): subprocess.run(['/Users/USER/.local/bin/ffmpeg','-v','error','-ss',str(start),'-i',str(source/src),'-t',str(dur),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
 return {'path':str(dest),'source':str(source/src),'sourceInSeconds':start,'duration':dur,'muted':True,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: rows=list(ex.map(make,clips))
files={'early.png':'03-实机素材/历史过程/p7-sentinel-side-20261021-085018.png','walk.mp4':'03-实机素材/动作测试/p13-r3-blender-walk-cycle.mp4','church.png':'03-实机素材/干净原图/p78-ue-church_fixed.png','tree.png':'03-实机素材/干净原图/p78-ue-tree.png','player.png':'03-实机素材/干净原图/p82-ue-player-Idle.png','died.png':'01-来源与对标/own-gameplay-20261023.png','prince.mp4':'01-来源与对标/little-prince-reference-480x270.mp4'}
for name,src in files.items():
 shutil.copy2(C/src,pub/name);rows.append({'path':str(pub/name),'source':str(C/src),'sha256':hashlib.sha256((pub/name).read_bytes()).hexdigest()})
(R/'evidence/full-media-preparation.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
# Exact source, only geometry for vertical and removal of unused private Sfx.
src=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/解包只读副本/fred-wave3-40-20261012/src/components/T17c-FileTree.tsx');s=src.read_text()
s=s.replace('Math.min(92, 860 / n)','Math.min(132, 1240 / n)').replace('Math.min(52, LH * 0.58, 1640 / needUnits)','Math.min(62, LH * 0.58, 920 / needUnits)').replace('556 - H / 2','970 - H / 2').replace('960 - treeW / 2, 960 - groupW / 2','540 - treeW / 2, 540 - groupW / 2').replace('width={1920} height={1080}','width={1080} height={1920}').replace('1920 - reveal','1080 - reveal')
s=s.replace('    {maxDepth > 0 && <Sfx name="slide" at={layerAt(1)} />}','').replace('    {litRows.map((_, k) => <Sfx key={k} name="pop" at={lightAt(k)} />)}','')
(R/'src/components/T17c-FileTree.tsx').write_text(s)
print('MEDIA_READY')
