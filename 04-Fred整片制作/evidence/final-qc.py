from pathlib import Path
import json,hashlib,subprocess,numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
frames=sorted(set(range(0,6241,60))|{599,600,735,736,777,778,1707,1708,1952,1953,2718,2719,3313,3314,3819,3820,4263,4264,4936,4937,5015,5060,5105,5160,5210,5260,5363,5364,5585,5586,6240})
files=sorted((R/'evidence/final-frames').glob('sample-*.png'));assert len(files)==len(frames),(len(files),len(frames))
for start in range(0,len(frames),24):
 sheet=Image.new('RGB',(1440,1440),'#ddd');d=ImageDraw.Draw(sheet)
 for k,(f,p) in enumerate(zip(frames[start:start+24],files[start:start+24])):
  im=Image.open(p);im.thumbnail((195,347));x=k%6*240;y=k//6*360;sheet.paste(im,(x,y+13));d.text((x,y),f'{f} / {f/60:.3f}s',fill='black')
 sheet.save(R/f'evidence/final-frames/contact-{start//24+1}.jpg')
(R/'evidence/final-frame-map.json').write_text(json.dumps([{'frame':f,'seconds':f/60,'path':str(p)} for f,p in zip(frames,files)],indent=2))
def samples(path):return np.frombuffer(subprocess.check_output(['/Users/USER/.local/bin/ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),dtype='<f4')
a=samples(R/'public/voice.wav');b=samples(R/'output/elden-ring-ai-recap-v1.mp4');n=min(len(a),len(b));a=a[:n];b=b[:n]
res={'sourceSamples':len(a),'finalSamples':len(b),'zeroLagCorrelation':float(np.corrcoef(a,b)[0,1]),'rmsGainDB':float(20*np.log10(np.sqrt(np.mean(b*b))/np.sqrt(np.mean(a*a)))),'peakDBFS':float(20*np.log10(np.max(np.abs(b)))),'method':'Decoded final AAC versus frozen master at identical sample clock; numeric signal comparison only, not hearing.'};(R/'evidence/audio-numeric-check.json').write_text(json.dumps(res,indent=2));print(res)
