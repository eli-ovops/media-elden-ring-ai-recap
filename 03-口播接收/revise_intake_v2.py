# coding: utf-8
from pathlib import Path
import json,subprocess,hashlib,wave,copy
p=Path(__file__).resolve().parent
old=json.loads((p/'源时码与剪辑EDL-v1.json').read_text())
bounds={3:(14/60,1722/60),2:(14/60,2570/60),1:(33/60,2010/60)}
ed=[];deleted=[];pos=0
for s in old['segments']:
 t=copy.deepcopy(s);a,b=bounds[s['attachment']];t.update(source_in=a,source_out=b,timeline_in=pos,timeline_out=pos+b-a,reason='只收头尾明确低电平准备/收尾，距检测语音活动约0.2秒，句内不剪');ed.append(t);pos+=b-a
 deleted.extend([dict(attachment=t['attachment'],source_in=0,source_out=a),dict(attachment=t['attachment'],source_in=b,source_out=s['source_out'])])
(p/'源时码与剪辑EDL-v2.json').write_text(json.dumps(dict(speed=1,duration=pos,segments=ed,deleted=deleted,precision='视频60fps格点；句内无剪切；头尾依据图像采样及音轨能量，不冒充听核'),ensure_ascii=False,indent=2))
rows=json.loads((p/'字幕重映射与校字-v1.json').read_text())['segments'];cues=[];changes=[]
for r in rows:
 i=r['attachment'];a=r['source_in'];b=r['source_out'];txt=r['text'].replace('这本大树守卫','这版大树守卫').replace('恶梦','噩梦')
 parts=[(a,b,txt)]
 if i==3 and a==0:parts=[(a,2.5,'玩过艾尔登法环的玩家'),(2.5,b,'应该都还记得有一个东西叫大树守卫')]
 if i==3 and a==8.44:parts=[(a,12.5,'然后前两天我让我的Codex'),(12.5,b,'帮我复刻了一版大树守卫')]
 if i==3 and a==16.04:parts=[(a,18.9,'我用的模型是Astra'),(18.9,b,'还有Sol 6.1的Ultra')]
 if i==1 and a==0:parts=[(a,3.35,'我做的这版大树守卫'),(3.35,b,'和我真的想要的')]
 if i==1 and a==11.76:parts=[(a,14.5,'我把源码还有模型的那些资源'),(14.5,b,'都已经放到GitHub了')]
 if i==1 and a==16.96:parts=[(a,20.6,'然后如果说有兴趣的大神的话'),(20.6,b,'可以去接着我的模型继续')]
 if i==1 and a==27.4:parts=[(a,30.5,'如果说你们有兴趣的话'),(30.5,b,'可以问我要GitHub的链接')]
 seg=next(s for s in ed if s['attachment']==i)
 for st,en,t in parts:
  st=max(st,seg['source_in']);en=min(en,seg['source_out']);assert st<en
  cues.append(dict(attachment=i,source_in=st,source_out=en,in_time=seg['timeline_in']+st-seg['source_in'],out_time=seg['timeline_in']+en-seg['source_in'],text=t))
 changes.append(dict(attachment=i,source_in=a,old=r['text'],new=txt,splits=parts))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'同步字幕-v2.srt').write_text('\n\n'.join(f'{n}\n{stamp(c["in_time"])} --> {stamp(c["out_time"])}\n{c["text"]}' for n,c in enumerate(cues,1))+'\n')
(p/'字幕重映射与校字-v2.json').write_text(json.dumps(dict(cues=cues,changes=changes,alignment='完整词/语义人工重分；新句内cue边界为候选，未词级听核；全片时间统一依EDLv2映射',brand_policy='Codex/Sol 6.1 Ultra/Opus 5.5/Token/GitHub/Astra/Blender完整拼写，声音不改，Claude仍为候选',pending='附件2源28.16—35.44工具名及整句听核，保留实录不补Tripo等旧稿'),ensure_ascii=False,indent=2))
inp=[];fs=[]
for k,s in enumerate(ed):
 inp+=['-i',s['path']];fs.append(f'[{k}:a]atrim=start={s["source_in"]}:end={s["source_out"]},asetpts=PTS-STARTPTS[a{k}]')
fs.append('[a0][a1][a2]concat=n=3:v=0:a=1[out]')
cmd=['/Users/USER/.local/bin/ffmpeg','-v','error','-n',*inp,'-filter_complex',';'.join(fs),'-map','[out]','-ar','48000','-ac','1','-c:a','pcm_s24le',str(p/'edit/voice-master-v2.wav')]
subprocess.run(cmd,check=True)
(p/'edit/生成参数-v2.json').write_text(json.dumps(dict(command=cmd,speed=1,gain_db=0,denoise=False,limiter=False),ensure_ascii=False,indent=2))
with (p/'edit/响度测量-v2.log').open('w') as out:subprocess.run(['/Users/USER/.local/bin/ffmpeg','-hide_banner','-i',str(p/'edit/voice-master-v2.wav'),'-af','ebur128=peak=true','-f','null','-'],stderr=out,stdout=subprocess.DEVNULL,check=True)
with wave.open(str(p/'edit/voice-master-v2.wav')) as w:real=w.getnframes()/w.getframerate()
r=json.loads((p/'03-接收报告-v1.json').read_text());r.update(version='v2',status='KNOWN_REVISIONS_COMPLETE_PENDING_PMO',raw_and_master_duration=pos,decoded_wav_duration_seconds=real,duration_note='EDLv2及master按同样头尾裁切，容器/解码样本微差另列',report=dict(send='PENDING',received='UNKNOWN',accepted='PENDING'))
r['edit'].update(wav='edit/voice-master-v2.wav',reason='只删六处头尾空段，安全余量约0.2秒，内部PCM不变',edl='源时码与剪辑EDL-v2.json');r['subtitles'].update(path='同步字幕-v2.srt',alignment='按完整词与语义重分；候选句内时码，仍待听核')
r['edge_review']=dict(evidence='edge-review-v2/edge-evidence-v2.json',frames='三张clipN-edges.jpg，每条头尾各三帧实际查看',scope='仅头尾约1秒；沿既有静音日志与本地解码WAV能量',saved_seconds=old['duration']-pos,safety_margin='头约0.175—0.202秒，尾约0.196—0.210秒',continuous_viewing=False)
r['file_inventory']='保留全部v1；新增v2 EDL/SRT/校字/master/参数/响度记录、局部头尾图与能量证据、重建脚本；没有清理。'
(p/'03-接收报告-v2.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
assert all(c['out_time']<=pos+.001 for c in cues)
for x,y in zip(cues,cues[1:]):assert x['out_time']<=y['in_time']+.001
assert all(not c['text'].endswith(('Cod','资','的')) for c in cues if c['text'].startswith(('然后前两天','我把源码','然后如果说')))
print(json.dumps(dict(edl_duration=pos,wav_duration=real,saved=old['duration']-pos,cues=len(cues),segments=ed),ensure_ascii=False,indent=2))
