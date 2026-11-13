# coding: utf-8
from pathlib import Path
import json,subprocess,hashlib,wave
p=Path(__file__).resolve().parent
m=json.loads((p/'原片清单-v1.json').read_text())
(p/'edit').mkdir(exist_ok=True)
order=[(3,28.973333),(2,43.025),(1,34.475)]
ed=[];pos=0
for i,end in order:
 f=m['files'][i-1];ed.append(dict(attachment=i,path=f['path'],source_in=0,source_out=end,timeline_in=pos,timeline_out=pos+end,reason='完整保留；语义重排，不凭ASR删句内原声'));pos+=end
(p/'源时码与剪辑EDL-v1.json').write_text(json.dumps(dict(speed=1,duration=pos,segments=ed,deleted=[],precision='完整原片边界，非音素级对齐'),ensure_ascii=False,indent=2))
fix={'大数所谓':'大树守卫','偷肯':'Token','圆码':'源码','放得给它':'放到GitHub','给它们的练结':'GitHub的链接','弓墊':'宫殿','opus5.5':'Opus 5.5','austra':'Astra','blander':'Blender','claw的':'Claude','爱顿法环':'艾尔登法环','大树手':'大树守','付科了一半':'复刻了一版','Soul6.1的Aut':'Sol 6.1的Ult'}
raw=[];cues=[];bodies=[]
for seg in ed:
 i=seg['attachment'];a=json.loads((p/'asr'/f'clip{i}.json').read_text())['transcription'];rows=[]
 for x in a:
  t=x['text'].strip()
  for old,new in fix.items():t=t.replace(old,new)
  r=dict(source_in=x['offsets']['from']/1000,source_out=min(x['offsets']['to']/1000,seg['source_out']),text=t,raw=x['text'],attachment=i)
  if t in ['卫','ra'] and rows:
   rows[-1]['text']+=t;rows[-1]['source_out']=r['source_out']
  else:rows.append(r)
 bodies.append('，'.join(r['text'] for r in rows))
 for r in rows:
  raw.append(r);t=r['text'];n=(len(t)+19)//20
  for j in range(n):
   txt=t[len(t)*j//n:len(t)*(j+1)//n];st=r['source_in']+(r['source_out']-r['source_in'])*j/n;en=r['source_in']+(r['source_out']-r['source_in'])*(j+1)/n
   cues.append((seg['timeline_in']+st,seg['timeline_in']+en,txt))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'同步字幕-v1.srt').write_text('\n\n'.join(f'{n}\n{stamp(a)} --> {stamp(b)}\n{t}' for n,(a,b,t) in enumerate(cues,1))+'\n')
(p/'字幕重映射与校字-v1.json').write_text(json.dumps(dict(segments=raw,corrections=fix,alignment='ASR片段时码；长句按比例拆候选，非逐字精对齐',pending='附件2源28.16—35.44工具链需听核；Claude是候选，不是已核作者事实'),ensure_ascii=False,indent=2))
(p/'实际口播与顺序-v1.md').write_text('# 实际口播与顺序v1\n\n顺序：附件3→2→1。以下完整本地ASR校字稿，非直接听音通过。\n\n'+'\n\n'.join(bodies)+'\n\n相对旧稿：实际说Codex、整整三天、差不多70亿、问我要链接；不补回骑兵站着我躺着、板甲球形关节、详细69.4亿、README等旧稿内容。保留自然口语与重复“烧不动”，没有确认失败重说，不仅凭ASR或静音阈值删声音。完整106.473333秒按语义拼接，保留原片头尾。\n\n待核：附件2源28.16—35.44工具链ASR含claw的/austra/blander，字幕Claude/Astra/Blender是候选，人工听核前不可称准确。附件3源24.6—28.28说差不多70亿，画面必须标账号三天总量69.4亿，不能游戏独占。附件1 GitHub名词为上下文校字待听核。没有把不确定识别当作口误删除。\n\n本轮各原片源2秒实看一帧，仅人物与画幅确认。未直接听音、未连续看听、未逐字精对齐。')
inputs=[];filters=[]
for k,s in enumerate(ed):
 inputs+=['-i',s['path']];filters.append(f'[{k}:a]atrim=start=0:end={s["source_out"]},asetpts=PTS-STARTPTS[a{k}]')
filters.append('[a0][a1][a2]concat=n=3:v=0:a=1[out]')
cmd=['/Users/USER/.local/bin/ffmpeg','-v','error','-n',*inputs,'-filter_complex',';'.join(filters),'-map','[out]','-ar','48000','-ac','1','-c:a','pcm_s24le',str(p/'edit/voice-master-v1.wav')]
subprocess.run(cmd,check=True)
(p/'edit/生成参数-v1.json').write_text(json.dumps(dict(command=cmd,speed=1,gain_db=0,denoise=False,limiter=False),ensure_ascii=False,indent=2))
print('duration',pos,flush=True)
