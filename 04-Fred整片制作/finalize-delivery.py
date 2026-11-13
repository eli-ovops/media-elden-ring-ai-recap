from pathlib import Path
import json,hashlib,sys,subprocess,copy,re
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
runtime=R.parents[1]/'deepseek-deepinfer-20261021/04-Fred整片重制/fred-runtime'
sys.path.insert(0,str(runtime/'skills/fred-remotion-output/scripts'))
from library_gate import acceptance_signature

def rec(p,**more):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**more}
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'Manifest.json').read_text())
final=rec(R/'output/elden-ring-ai-recap-v1.mp4',durationSeconds=6241/60,frames=6241,width=1080,height=1920,fps=60,bytes=(R/'output/elden-ring-ai-recap-v1.mp4').stat().st_size)
coverNames=['cover-3x4-1080x1440-v1.png','cover-9x16-1080x1920-v2.png','cover-16x9-1920x1080-v1.png','cover-4x3-1440x1080-v1.png']
covers=[];sheet=Image.new('RGB',(1080,520),'#eee');draw=ImageDraw.Draw(sheet)
for i,name in enumerate(coverNames):
 p=R/'covers'/name;im=Image.open(p);covers.append(rec(p,width=im.width,height=im.height));im.thumbnail((252,450));sheet.paste(im,(i*270,30));draw.text((i*270+4,8),name.split('-')[1],fill='black')
sheet.save(R/'covers/phone-review.jpg');save(R/'covers/dimensions-sha.json',covers)
coverReview={'status':'SCOPED_VISUAL_REVIEW','current':covers,'identityReference':rec(Path('/Volumes/EXTERNAL/自媒体/人物形象与封面资产-20261009/外部艺术照精选-20261009/入选/02-思考分析-图5-深蓝衬衫.png')),'prompts':[rec(p) for p in sorted((R/'covers/prompts').glob('*.json'))],'generatedOriginals':[rec(p) for p in sorted((R/'covers').glob('*generated*.png'))],'method':'4 separate imagegen compositions plus 3 targeted imagegen corrections; proportional resizing and white padding only for exact output dimensions; no stretch or blind crop.','checks':'All four full images reviewed, exact dimensions verified. Latest 9x16 v2 corrected weapon edge; current titles remain AI复刻大树守卫 / 三天后 / 长这样 in black/black/purple. Identity likeness and subject/title margins inspected. Phone contact sheet contains current four outputs.','acceptance':'PMO/user PENDING','history':'9x16 normalized v1 and generated v1 variants retained as historical, excluded from delivery.'}
save(R/'covers/cover-review-v1.json',coverReview)
frames=json.loads((R/'evidence/final-frame-map.json').read_text())
for p in m['pages']:
 if p['implementationMode']!='adapted':continue
 p['keyframeReview']['frames']=[rec(f['path'],frame=f['frame'],seconds=f['seconds'],origin='actual final MP4 decoded frame',sourceVideoSha256=final['sha256']) for f in frames if p['startFrame']<=f['frame']<p['startFrame']+p['durationInFrames']]
 p['keyframeReview']['coverage']='Actual export sparse frame inspection at 360x640 plus prior full-resolution component intermediate states; not continuous motion review.'
 p['componentAcceptance']['checks']['finalExport']='实际完整MP4采样对照已查看；源组件与当前调用SHA一致。账号数字26.3/24.3/18.8与总计69.4、目录树展开/黑条中态/终态在已检采样中保持原组件关系。不是连续视听PASS。'
m['status']='PRODUCTION_COMPLETE_SCOPED_SELF_CHECK';m['finalOutput']=final;m['covers']=covers
m['reviewLimits']['sourceCrop']='约67–70秒第三方原片背景英文句子被竖屏裁切，主要作者场景主体与本期中文字幕可见；未宣称保留原片所有画面文字。'
m['reviewLimits']['externalAcceptance']='PMO full-film review / 05 independent review / user final review PENDING'
m['reviewLimits']['sampling']='Sparse actual-export frames and contact sheets, not continuous normal-speed playback or all-frame inspection.'
m['preview']={'url':'http://127.0.0.1:55323/preview.html','server':str(R/'preview-server.cjs'),'bind':'127.0.0.1','seekable':[0,104.016667],'directHearing':'UNKNOWN'}
m['finalChecks']={'probe':rec(R/'evidence/final-probe.json'),'decode':rec(R/'evidence/final-decode-errors.txt',status='PASS_EMPTY_ERROR_LOG'),'frameMap':rec(R/'evidence/final-frame-map.json',count=len(frames)),'audioNumeric':rec(R/'evidence/audio-numeric-check.json'),'covers':rec(R/'covers/cover-review-v1.json')}
for stage in ['suggestion','keyframes']:
 for p in m['pages']:
  if p['implementationMode']!='adapted':continue
  p['componentAcceptance'].update(stage=stage,evidence=p['keyframeReview']['frames'],contextSha256=acceptance_signature(m,p,stage))
 snap=R/f'evidence/Manifest-final-{stage}.json';save(snap,m)
 out=R/f'evidence/gate-final-{stage}.json'
 result=subprocess.run([sys.executable,str(runtime/'skills/fred-remotion-output/scripts/library_gate.py'),'--manifest',str(snap),'--stage',stage,'--output',str(out)],text=True,capture_output=True)
 print(stage,result.stdout,result.stderr)
 if result.returncode:raise SystemExit(result.returncode)
save(R/'Manifest.json',m)
blocks=re.split(r'\n\s*\n',(R/'output/elden-ring-ai-recap-v1.srt').read_text().strip())
(R/'output/actual-speech-v1.md').write_text('# 本期实际口播与字幕\n\n当前104.016667秒，60fps/6241帧；来自冻结同步字幕-v2.srt，共39条。句内时码与工具名听核仍为候选，未作直接听音PASS。旧actual-speech-source.md仅历史理解稿，其旧时长不作当前依据。\n\n'+'\n\n'.join('**'+b.splitlines()[1]+'**  \n'+''.join(b.splitlines()[2:]) for b in blocks)+'\n')
assert len(blocks)==39
pub=[rec(p,relative=str(p.relative_to(R))) for p in sorted((R/'public').rglob('*')) if p.is_file()]
save(R/'evidence/project-media-inventory.json',pub)
versions={name:json.loads((R/'node_modules'/name/'package.json').read_text())['version'] for name in ['remotion','@remotion/renderer','@remotion/bundler','react','react-dom']}
save(R/'evidence/runtime-dependencies.json',{'versions':versions,'nodeModulesRealPath':str((R/'node_modules').resolve()),'note':'Reuses existing local dependencies via symlink; package manager lockfile not supplied by this project. Not a standalone installed bundle.'})
preview={'url':m['preview']['url'],'observedAt':'2026-10-23','browser':'Codex IAB','video':{'duration':104.016667,'width':1080,'height':1920,'readyState':4,'seekable':[[0,104.016667]],'error':None},'images':covers,'rangeProbe':{'status':206,'contentRange':'bytes 100-199/164559034'},'limit':'Metadata/range/load check only; no direct audio or normal-speed continuous AV acceptance.'}
save(R/'evidence/preview-check-v1.json',preview)
qa={'content_id':m['content_id'],'owner':'04','status':'PRODUCTION_COMPLETE_SCOPED_SELF_CHECK','finalOutput':final,'coverage':{'decodedAV':'complete file; error log empty','actualExportSampleFrames':len(frames),'contactSheets':6,'visualMethod':'1fps plus selected seams and component middle states; all 6 contact sheets reviewed. 360x640 samples; representative and T17c native stills reviewed earlier.','observations':'已检采样中本人头脸、字幕与实材主体可见；无采样黑帧/白闪；39条字幕按冻结源时钟。原行走片仅0.7秒一次，不循环伪造长实机。','sources':'T14e / T17c exact source+kit, actual import/call/output hashes bound in Manifest; reference preview contact sheets previously viewed.','audioNumeric':json.loads((R/'evidence/audio-numeric-check.json').read_text()),'audioNumericCaveat':'Counts in numeric report are aligned minimum comparison length, not independent full decoded length. Container audio duration104.016000 vs video104.016667 differs0.000667 seconds. Signal comparison is not hearing.','covers':rec(R/'covers/cover-review-v1.json'),'preview':rec(R/'evidence/preview-check-v1.json')},'gates':{s:rec(R/f'evidence/gate-final-{s}.json') for s in ['suggestion','keyframes']},'limits':m['reviewLimits'],'acceptances':{'representativePMO':'PASS_FOR_FULL_PRODUCTION_SCOPED','fullPMO':'PENDING','independent05':'NOT_RELEASED_BY_PMO','user':'PENDING','published':'NO'},'recovery':'Existing render DONE verified after app interruption; reused file, no duplicate render. Current final voice mux and evidence completed.'}
save(R/'04-完整成片自检-v1.json',qa)
print(json.dumps({'final':final,'frames':len(frames),'covers':covers,'versions':versions},ensure_ascii=False,indent=2))
