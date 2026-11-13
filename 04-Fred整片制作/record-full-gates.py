import json,hashlib,sys,copy,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent; root=R.parents[1]/'deepseek-deepinfer-20261021/04-Fred整片重制/fred-runtime';sys.path.insert(0,str(root/'skills/fred-remotion-output/scripts'))
from library_gate import load_catalog,acceptance_signature
from component_selection import shortlist
from common import load_references
def rec(p,**x):p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**x}
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'Manifest.json').read_text());plan=R/'evidence/planning-Manifest-v1.json'
if not plan.exists():save(plan,m)
old=json.loads(plan.read_text());account=copy.deepcopy(next(x for x in old['pages'] if x['stableId']=='account'));pages=[]
segments=[('opening',0,600,'talk-1.mp4',0),('early',600,736,'early.png',0),('walk',736,778,'walk.mp4',0),('church',778,948,'church.png',0),('models',948,1120,'talk-1.mp4',15.8),('tree',1120,1224,'tree.png',0),('sentinel',1224,1344,'sentinel.png',0),('account',1344,1708,None,0),('motivation',1708,1953,'talk-2.mp4',0),('prince',1953,2719,'prince-720.mp4',2),('try',2719,3124,'talk-2.mp4',(2719-1708)/60),('duration',3124,3314,'prince-720.mp4',12),('tools',3314,3820,'talk-2.mp4',(3314-1708)/60),('prince-result',3820,4264,'prince-720.mp4',42),('player-result',4264,4432,'player.png',0),('died',4432,4567,'died.png',0),('gap',4567,4721,'talk-3.mp4',(4567-4264)/60),('tokens',4721,4937,'talk-3.mp4',(4721-4264)/60),('handoff',4937,5364,None,0),('handoff-sentinel',5364,5467,'sentinel.png',0),('handoff-player',5467,5586,'player.png',0),('closing',5586,6241,'talk-3.mp4',(5586-4264)/60)]
for sid,a,b,file,start in segments:
 if sid=='account':
  p=account;p['referenceChoices'][0]['callSite']=rec(R/'src/full-index.tsx',symbol='AccountScene',callee='StatTriplet');p['keyframeReview']['sourceFiles'][0]=rec(R/'src/full-index.tsx')
 elif sid=='handoff':
  cat=json.loads((R/'evidence/reference/handoff-catalog.json').read_text());selected=next(x for x in cat if x['label']=='T17c');reasons={'fred-wave3-40-t17c':'原预览同一树逐层展开和原位黑条说明，符合真实仓库结构与模型位置。','fred-wave3-40-t02h':'三文件翻面强调用途说明，不适合本段源码与模型层级路径。','library-legacy81-r005':'数值拆分成分类数量，本期没有分类计数，拒绝。'}
  p={'stableId':sid,'implementationMode':'adapted','oneQuestion':'GitHub源码与模型资源在哪里','sceneGuide':{'type':'relationship'},'componentPlan':{'query':'文件夹 打开 文件 取出 展开','candidates':[{'id':x['id'].removeprefix('component:'),'decision':'selected' if x['label']=='T17c' else 'rejected','reason':reasons[x['id'].removeprefix('component:')]} for x in cat],'inspectedReferences':[rec(x['media']['path'],id=x['id'].removeprefix('component:'),observations=reasons[x['id'].removeprefix('component:')],sampling='2fps actual preview contact sheet',contactSheet=rec(R/f"evidence/reference/{x['label']}.jpg")) for x in cat]},'referenceChoices':[{'id':'fred-wave3-40-t17c','reason':reasons['fred-wave3-40-t17c'],'preserve':'整棵树逐层连续让位展开、同一行黑条擦过反白到注释列、完整原kit字体阴影/路径关系。','change':'已核实际恢复结构8行、四条注释及cue；原生1080x1920，LH132、中心540/970、最大组宽920；不带私人音效或品牌。','useScope':'82.283333–89.4秒源码与模型接力；资料是仓库源码加Release恢复后的目录，不把Release当Git文件。','source':rec(selected['sources'][0]['path'],symbol='FileTree'),'implementation':rec(R/'src/components/T17c-FileTree.tsx',symbol='FileTree'),'callSite':rec(R/'src/full-index.tsx',symbol='HandoffScene',callee='FileTree'),'kitSources':[rec(x['path']) for x in selected['kits']],'kitActual':[rec(R/'src/kit/theme.ts'),rec(R/'src/kit/ui.tsx')]}], 'keyframeReview':{'frames':[rec(R/f'evidence/full-stills/f{f}.png',frame=f) for f in [4955,5015,5060,5105,5160,5210,5260,5320,5363]],'sourceFiles':[rec(R/'src/full-index.tsx'),rec(R/'src/components/T17c-FileTree.tsx'),rec(R/'src/kit/theme.ts'),rec(R/'src/kit/ui.tsx')]}}
 else:
  p={'stableId':sid,'implementationMode':'preserved-media','referenceChoices':[],'mediaContract':[rec(R/'public'/file,sourceInSeconds=start)],'componentPlan':{'search':'not-needed','decisionReason':'实际原声真人或有出处游戏/作者原媒体保真剪切；无新增近似重画组件。'}}
 p.update(startFrame=a,durationInFrames=b-a);pages.append(p)
prince=next(x for x in pages if x['stableId']=='prince');prince['mediaContract'][0]['segments']=[{'outputFrames':[1953,2364],'sourceInSeconds':2},{'outputFrames':[2364,2558],'sourceInSeconds':6},{'outputFrames':[2558,2632],'sourceInSeconds':18.3},{'outputFrames':[2632,2719],'sourceInSeconds':40}]
next(x for x in pages if x['stableId']=='tools')['selectionNote']='已看T18b/102-01/T04b准确原预览；前者隐含工作流，中者四作品变成两品牌，后者固定分工，均不符合本期仅口述工具组合。保持真人和源字幕，不强加因果链。'
m['pages']=pages;m['status']='FULL_PRODUCTION';m['referenceCatalogRevision']=load_catalog()['revision'];m['representative']['pmoAcceptance']=rec(R/'PMO-代表片段对照验收-v1.json');m['mediaPreparation']=rec(R/'evidence/full-media-preparation.json');m['newSource']=rec(R/'evidence/prince-hd-transfer.json');m['entryPoint']=str(R/'src/full-index.tsx');m['reviewLimits']['directHearing']='UNKNOWN; PMO范围补充明确不阻断制作，用户终审PENDING';m['referenceSources']=[{'url':'https://x.com/Saccc_c/status/2109962425512734739','media':'public/prince-720.mp4','scope':'attributed short critique excerpts, original audio muted'}, {'url':'https://github.com/eli-ovops/AI-Limgrave-Lab','verifiedAt':'2026-10-23','facts':'Source/ Content/ assets/blender/ assets/export/ 按README真实恢复结构，后3类在Release中'}]
for stage in ['suggestion','keyframes']:
 for p in pages:
  if p['implementationMode']!='adapted':continue
  if p['stableId']=='account':checks=copy.deepcopy(account['componentAcceptance']['checks'])
  else:checks={'semanticFit':'源码与Release资源的真实目录层级，非下载即玩。','corePreserved':'原T17c完整FileTree、Icon、rowContent、Handoff、w/shown/ys/lines和黑条反白实现；仅本期内容和竖屏几何。','visualQuality':'已看f4955至5363的原生竖屏展开、标注和终态；f5060原尺寸确认黑条中态是源擦过动作，右侧尚未显出不是文字裁断；全部终态在1080范围内。'}
  p['componentAcceptance']={'status':'passed','reviewer':'assistant','stage':stage,'checks':checks,'evidence':[p['keyframeReview']['frames'][-1]],'contextSha256':acceptance_signature(m,p,stage)}
 save(R/f'evidence/Manifest-full-{stage}.json',m)
 result=subprocess.run([sys.executable,str(root/'skills/fred-remotion-output/scripts/library_gate.py'),'--manifest',str(R/f'evidence/Manifest-full-{stage}.json'),'--stage',stage,'--output',str(R/f'evidence/gate-full-{stage}.json')],capture_output=True,text=True)
 print(result.stdout);print(result.stderr)
 if result.returncode:raise SystemExit(result.returncode)
save(R/'Manifest.json',m)
