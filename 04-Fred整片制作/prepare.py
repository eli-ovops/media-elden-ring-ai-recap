from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parent; ROOT=Path('/Users/USER/.codex/skill-repos/FredTalk'); E=R/'evidence'; E.mkdir(exist_ok=True)
def rec(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
edl=json.loads((R.parent/'03-口播接收/源时码与剪辑EDL-v2.json').read_text())
rows=[('opening',0,8.2,None,'','法环新手与大树守卫'),('recreation',8.2,15.8,None,'','Codex复刻真实结果'),('models',15.8,22.4,'relationship','两项 工具 卡片 并排 展示','Astra与Sol 6.1 Ultra'),('account',22.4,28.4666666667,'metric-change','数字 累加 汇总 计数','三天账号用量69.4亿'),('motivation',28.4666666667,32.55,None,'','为什么忽然想做游戏'),('prince',32.55,45.3166666667,None,'','小王子的草地宫殿玫瑰花园'),('try',45.3166666667,52.0666666667,None,'','为什么我不能试一下'),('duration',52.0666666667,56.4,'metric-change','数字 时间 天数 重点 放大','作者16天'),('tools',56.4,63.6666666667,'relationship','多个 工具 图标 集合 环绕 中心','作者工具组合'),('prince-result',63.6666666667,71.0666666667,None,'','优化与修Bug后的小王子'),('gap',71.0666666667,78.6833333333,None,'','我做的这版与期待仍有差距'),('tokens',78.6833333333,82.2833333333,None,'','烧不动Token'),('handoff',82.2833333333,95,'relationship','文件 包 模型 源码 分享 接力 展开','源码和模型已放GitHub供继续'),('closing',95,104.0166666667,None,'','有兴趣问我要GitHub链接')]
m={'content_id':'elden-ring-ai-recap-20261023','version':'v1','status':'PLANNING','timelineFps':60,'durationInFrames':6241,'outputSpec':{'width':1080,'height':1920,'fps':60},'workflow':{'profile':'fred-video-v2','componentMatching':'v1'},'audio':rec(R.parent/'03-口播接收/edit/voice-master-v2.wav'),'subtitles':rec(R.parent/'03-口播接收/同步字幕-v2.srt'),'edl':rec(R.parent/'03-口播接收/源时码与剪辑EDL-v2.json'),'rules':{'project':'ELI-MEDIA-AGENTS-20261022-v3','method':'ELI-PRODUCTION-20261022-v4','rework':'ELI-REWORK-20261019-v1'},'routing':{'target':'gpt-6-astra/high','actualModel':'UNKNOWN','actualEffort':'UNKNOWN'},'reviewLimits':{'directHearing':'UNKNOWN; PMO已报告需安排承担方','continuousAV':'UNKNOWN','subtitlePrecision':'候选句内时码，未作听核PASS'},'pages':[]}
for sid,a,b,typ,q,txt in rows:
 p={'stableId':sid,'startFrame':round(a*60),'durationInFrames':round(b*60)-round(a*60),'oneQuestion':txt,'sourceSpans':[{'text':txt}],'implementationMode':'adapted' if typ else 'preserved-media','referenceChoices':[]}
 if typ:p.update(sceneGuide={'type':typ},componentPlan={'query':q})
 else:p['mediaContract']=[dict(rec(s['path']),sourceInSeconds=s['source_in']+max(a-s['timeline_in'],0),sourceOutSeconds=s['source_in']+min(b-s['timeline_in'],s['timeline_out']-s['timeline_in'])) for s in edl['segments'] if a<s['timeline_out'] and b>s['timeline_in']]
 m['pages'].append(p)
(R/'Manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for p in m['pages']:
 if p['implementationMode']=='preserved-media':continue
 out=subprocess.check_output(['python3',str(ROOT/'skills/fred-remotion-output/scripts/scene.py'),'--project-root',str(ROOT),'--manifest',str(R/'Manifest.json'),'--scene-id',p['stableId'],'--candidates-only'])
 (E/(p['stableId']+'-candidates.json')).write_bytes(out)
 d=json.loads(out);print(p['stableId'],[(x['label'],x['title']) for x in d['libraryCandidates']['candidates'][:3]])
