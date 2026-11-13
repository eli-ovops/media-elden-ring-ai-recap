import json,hashlib,sys,copy,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]; root=R.parents[1]/'deepseek-deepinfer-20261021/04-Fred整片重制/fred-runtime'; sys.path.insert(0,str(root/'skills/fred-remotion-output/scripts'))
from library_gate import load_catalog,acceptance_signature
from component_selection import shortlist
from common import load_references
def rec(p,**extra):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**extra}
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'Manifest.json').read_text());p=next(x for x in m['pages'] if x['stableId']=='account'); c=json.loads((R/'evidence/reference/catalog-selected.json').read_text()); sel=next(x for x in c if x['label']=='T14e');_,normalized=load_references(root)
reasons={'fred-wave3-40-t14e':'实际预览保留并列数值错峰落定及末卡黑紫突出，直接表达三日数值与总量。','fred-native-t14c':'实际预览有旧价划线和差额标签；本期是账号总量，不是降价，故拒绝。','fred-wave3-40-t15e':'实际预览逐段折线、坐标轴及高亮点；本段只讲总量，无趋势结论，故拒绝。'}
p['componentPlan']['candidates']=[{'id':x['id'],'decision':'selected' if x['id']==sel['id'].removeprefix('component:') else 'rejected','reason':reasons[x['id']]} for x in shortlist(root,normalized,p,3)['candidates']]
p['componentPlan']['inspectedReferences']=[rec(x['media']['path'],id=x['id'].removeprefix('component:'),observations=reasons[x['id'].removeprefix('component:')],sampling='2 fps contact sheet; not continuous audiovisual',contactSheet=rec(R/f"evidence/reference/{x['label']}.jpg")) for x in c]
p['referenceChoices']=[{'id':'fred-wave3-40-t14e','reason':reasons['fred-wave3-40-t14e'],'preserve':'StatTriplet完整逐卡rise、并行滚动/错峰落定、落定回弹、hero黑紫渐变/缩放、字形与阴影；原theme和UI实现。','change':'四项实数/日期/单位、cues .2/3.1；横排改竖屏2x2几何，Frame原生1080x1920；关闭私人品牌及未核音效。','useScope':'本代表片段local2.000–8.066667秒，对应整片22.4–28.466667；没有跨栈重画。','source':rec(sel['sources'][0]['path'],symbol='StatTriplet'),'implementation':rec(R/'src/components/T14e-StatTriplet.tsx',symbol='StatTriplet'),'callSite':rec(R/'src/index.tsx',symbol='AccountScene',callee='StatTriplet'),'kitSources':[rec(x['path']) for x in sel['kits']],'kitActual':[rec(R/'src/kit/theme.ts'),rec(R/'src/kit/ui.tsx')]}]
frames=[rec(R/f'evidence/stills/export-{i:02d}.png',frame=f,globalFrame=f+1224) for i,f in enumerate([100,119,120,135,170,240,310,370,482,483,484,485,540,650,728],1)]
p['keyframeReview']={'frames':frames,'sourceFiles':[rec(R/'src/index.tsx'),rec(R/'src/components/T14e-StatTriplet.tsx'),rec(R/'src/kit/theme.ts'),rec(R/'src/kit/ui.tsx')],'method':'实际MP4抽帧15张＋联系表＋f370原尺寸查看；原预览2fps采样；非连续视听。'}
checks={'semanticFit':'26.3/24.3/18.8对应三天账号数据，69.4为和；顶部账号限定清楚，不表示游戏专属或现金。','corePreserved':'原实现4卡的rise/roll/landed/heroP/heroQ及Surface关系保留；竖屏2x2呈现与原预览阶段一致。','visualQuality':'实际导出f135/170入场和滚动、f240/310落定、f370突出、f482/483末态以及f484/485真人回场已采样；f370原尺寸数字单位完整，手机联系表无裁字；黑紫变化保留。'}
m['referenceCatalogRevision']=load_catalog()['revision']; m['status']='REPRESENTATIVE_REVIEW_PENDING';m['representative']={'path':str(R/'output/representative-v1.mp4'),'sha256':rec(R/'output/representative-v1.mp4')['sha256'],'globalRangeSeconds':[20.4,32.55],'durationSeconds':12.15,'frames':729,'pmoAcceptance':'PENDING','hearing':'UNKNOWN','continuousAV':'UNKNOWN'}
scope=copy.deepcopy(m);scope['scope']='Representative only; no full-film gate claim';scope['pages']=[{'stableId':'representative-game','implementationMode':'preserved-media','mediaContract':[rec(R/'public/sentinel.png')]},copy.deepcopy(p),copy.deepcopy(next(x for x in m['pages'] if x['stableId']=='motivation'))]
for stage in ['suggestion','keyframes']:
 q=scope['pages'][1]; q['componentAcceptance']={'status':'passed','reviewer':'assistant','stage':stage,'checks':checks,'evidence':[rec(R/'evidence/reference/T14e.jpg'),rec(R/'evidence/stills/export-contact.jpg'),frames[7]],'contextSha256':acceptance_signature(scope,q,stage)}
 path=R/f'evidence/Manifest-representative-{stage}.json';save(path,scope)
 result=subprocess.run([sys.executable,str(root/'skills/fred-remotion-output/scripts/library_gate.py'),'--manifest',str(path),'--stage',stage,'--output',str(R/f'evidence/gate-representative-{stage}.json')],text=True,capture_output=True)
 print(result.stdout);print(result.stderr)
 if result.returncode:raise SystemExit(result.returncode)
p['componentAcceptance']=copy.deepcopy(scope['pages'][1]['componentAcceptance']);save(R/'Manifest.json',m)
qc={'scope':'Representative v1 only; global20.4–32.55s','output':rec(R/'output/representative-v1.mp4'),'spec':{'width':1080,'height':1920,'fps':60,'videoFrames':729,'durationSeconds':12.15,'audio':'AAC 48kHz mono'},'decode':{'status':'PASS','method':'ffmpeg full AV decode to null exit0; no error output'},'sourceAudio':{**m['audio'],'trimStartSeconds':20.4,'trimDurationSeconds':12.15,'gainDB':0,'speed':1,'processing':'AAC mux only, no second denoise'},'visualReview':{'status':'SCOPED_PASS_FOR_PMO_REVIEW','frames':frames,'checks':checks,'referenceOriginalSeconds':[0,5.012],'referenceOutputLocalSeconds':[2,8.066667]},'limitations':{'directHearing':'UNKNOWN','continuousAV':'UNKNOWN','sourceSpeechSubtitlePrecision':'03 SRT候选句内时码；没有听核PASS','gameSource':'1280x720真实静帧，竖屏cover裁切；非连续游戏，边缘盾牌裁切但人物骑乘主体可辨','subtitleBoundary':'local8.066667首真人帧无字幕，下一帧出现；来自SRT28.467毫秒舍入，无额外语音剪切'},'pmoAcceptance':'PENDING','userAcceptance':'PENDING','fullFilmStatus':'not rendered'}
save(R/'04-代表片段自检-v1.json',qc)
print('OUTPUT_SHA',qc['output']['sha256'])
