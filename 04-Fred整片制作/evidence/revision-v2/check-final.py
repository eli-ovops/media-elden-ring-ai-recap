from pathlib import Path
import subprocess,json,os
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];E=R/'evidence/revision-v2/final';E.mkdir(exist_ok=True);V=R/'output/elden-ring-ai-recap-v2-final.mp4'
ff='/Users/USER/.local/bin/ffmpeg'
probe='/Volumes/EXTERNAL/自媒体/Fred复刻测试-20261016/7694088597179239690/source-snapshot/FredTalk-1.5-3D/camera/node_modules/@remotion/compositor-darwin-arm64/ffprobe'
env=dict(os.environ,DYLD_LIBRARY_PATH=str(Path(probe).parent))
p=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(V)],env=env));(E/'probe-v2.json').write_text(json.dumps(p,indent=2))
v=next(s for s in p['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['nb_frames'],v['r_frame_rate'])==(1080,1920,'6241','60/1')
records=[]
for name,a,b,extras in [('cloud',1952,2559,[1952,1953,1954,2363,2364,2520,2557,2558,2559]),('relation',3967,4221,[3967,3968,3969,4020,4218,4219,4220,4221])]:
 frames=sorted(set(extras)|({2397,2407,2555,2556} if name=='cloud' else set()));folder=E/(name+'-export');folder.mkdir(exist_ok=True)
 expression='+'.join('eq(n\\,%d)'%(f-a) for f in frames)
 cmd=[ff,'-v','error','-ss',str(a/60),'-i',str(V),'-t',str((b-a+1)/60),'-vf','select='+expression+',scale=360:640','-fps_mode','vfr',str(folder/'f-%03d.png')]
 subprocess.run(cmd,check=True)
 files=sorted(folder.glob('f-*.png'));assert len(files)==len(frames),(name,len(files),len(frames))
 for f,file in zip(frames,files):records.append({'frame':f,'seconds':f/60,'path':str(file),'range':name})
 for start in range(0,len(files),18):
  sheet=Image.new('RGB',(1440,1200),'#eee');d=ImageDraw.Draw(sheet)
  for i,(f,file) in enumerate(zip(frames[start:start+18],files[start:start+18])):
   im=Image.open(file);im.thumbnail((216,384));x=i%6*240;y=i//6*400;sheet.paste(im,(x,y+15));d.text((x,y),str(f)+' / '+str(round(f/60,3)),fill='black')
  sheet.save(E/f'{name}-export-contact-{start//18+1}.jpg')
(E/'targeted-frame-map.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
for f in [2520,4020]:subprocess.run([ff,'-v','error','-ss',str(f/60),'-i',str(V),'-frames:v','1',str(E/f'actual-f{f}.png')],check=True)
print('Spec PASS; targeted frames',len(records))
