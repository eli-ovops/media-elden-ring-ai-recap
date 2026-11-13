from pathlib import Path
import json,hashlib,copy,re
R=Path(__file__).resolve().parent;E=R/'evidence/revision-v2'
def rec(p,**x):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**x}
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
v1=json.loads((R/'Manifest-v1.json').read_text());m=copy.deepcopy(v1)
final=rec(R/'output/elden-ring-ai-recap-v2-final.mp4',frames=6241,durationSeconds=6241/60,width=1080,height=1920,fps=60)
basecode=(E/'full-index-v1.tsx').read_text();newcode=(R/'src/full-index.tsx').read_text()
for symbol in ['AccountScene','HandoffScene']:
 a=next(line for line in basecode.splitlines() if line.startswith('export const '+symbol))
 b=next(line for line in newcode.splitlines() if line.startswith('export const '+symbol));assert a==b,symbol
preserved=[]
for p in m['pages']:
 if p['implementationMode']=='adapted':
  for choice in p['referenceChoices']:
   for asset in [choice['implementation'],*choice['kitActual']]:
    assert rec(asset['path'])['sha256']==asset['sha256'];preserved.append(asset)
   choice['callSite']=rec(R/'src/full-index.tsx',symbol=choice['callSite']['symbol'],callee=choice['callSite']['callee'])
  p['baselineAcceptance']=p.pop('componentAcceptance');p['componentAcceptance']={'status':'INHERITED_UNCHANGED_COMPONENT','scope':'v1准确组件/kit/内容/动作原件验收沿用；本轮仅Prince媒体取景和时钟变化，不重新签v2组件视觉PASS。','baselineManifest':str(R/'Manifest-v1.json')}
  p['keyframeReview']['scope']='v1实际导出证据，当前组件内容/实现未改；本轮不重复提取未变区间。'
 if p['stableId']=='prince':
  p['mediaContract'][0]['sourceInSeconds']=1.5
  p['mediaContract'][0]['segments']=[{'outputFrames':[1953,2558],'sourceInSeconds':1.5,'sourceOutSeconds':1.5+605/60,'camera':'actual prince position tracking, continuous source clock'}, {'outputFrames':[2558,2632],'sourceInSeconds':18.3},{'outputFrames':[2632,2719],'sourceInSeconds':40}]
 if p['stableId']=='prince-result':p['geometryRevision']={'frames':[3968,4220],'sourceRangeSeconds':[44.4666666667,48.6666666667],'viewport':[0,495,1080,810],'cropSourceApprox':[160,0,960,720],'reason':'保留王子左/狐狸右完整关系与原句；窗口变化卡在原片真实场景切换帧，前后原媒体时钟不变。'}
for c in m['covers']:assert rec(c['path'])['sha256']==c['sha256']
assert rec(m['subtitles']['path'])['sha256']==m['subtitles']['sha256']
(R/'output/elden-ring-ai-recap-v2.srt').write_bytes(Path(m['subtitles']['path']).read_bytes())
m.update(version='v2',status='TARGETED_REVISION_COMPLETE_PENDING_PMO',finalOutput=final)
m['reviewLimits'].pop('sourceCrop',None)
m['reviewLimits']['continuousAV']='UNKNOWN; 本轮只新增修复区间及接缝实际导出帧检查'
m['reviewLimits']['externalAcceptance']='PMO v2 / 05 / user PENDING'
m['reviewLimits']['sourceCropFix']='v1 C1/C2/C3已按定向修复；以本轮实际输出证据为准，不再将主体丢失作为可放行限制。'
m['revision']={'request':rec(R/'PMO-完整片定向返修-v1.json'),'baseline':rec(R/'Manifest-v1.json'),'modifiedFrameRanges':[[1953,2558],[3968,4220]],'sourceClockCloud':'source=1.5+(globalFrame-1953)/60; one sequence, no boundary/reset at2364','patches':[rec(R/'output/revision-v2-cloud-fixed.mp4'),rec(R/'output/revision-v2-relation.mp4')],'assembly':rec(R/'assemble-revision-v2.sh'),'assemblyLog':rec(E/'assembly-final.log'),'method':'仅857个受影响帧的最终补片。按精确帧时钟覆盖v1解码画面后编码完整视频，未用GOP切块拼接；未变画面保留原帧时序但因重编码不宣称视频字节相同。AAC直接stream copy。','componentPreservation':preserved}
m['finalChecks']={'baselineV1Only':v1['finalChecks'],'currentProbe':rec(E/'final/probe-v2.json'),'targetedFrameMap':rec(E/'final/targeted-frame-map.json'),'notRepeated':['ASR','audio numeric analysis','full decode verification','unaffected full-film/contact-sheet tests','Fred component rendering/gates','cover generation/review']}
m['preview']['url']='http://127.0.0.1:55323/preview-v2.html'
save(R/'Manifest-v2.json',m);save(R/'Manifest.json',m)
frames=json.loads((E/'final/targeted-frame-map.json').read_text())
qa={'content_id':m['content_id'],'version':'v2','owner':'04','status':'TARGETED_SELF_CHECK_COMPLETE_PMO_PENDING','output':final,'request':m['revision']['request'],'fixes':[{'id':'C1','change':'云海原序列一次连续播放，按原源人物位置设置跟随；42秒人物完整可见。','evidence':'evidence/revision-v2/final/actual-f2520.png'},{'id':'C2','change':'原1953→2364及2364→2558两段合为1953→2558；source1.5→11.583333，原2363/2364处source8.333333→8.35，无回跳。','evidence':'evidence/revision-v2/final/targeted-frame-map.json'},{'id':'C3','change':'只在真实狐狸镜头f3968–4219改为1080×810全宽较宽取景；两主体和英文原句完整，f4220按源切回原火车镜头。','evidence':'evidence/revision-v2/final/actual-f4020.png'}],'checks':{'probe':rec(E/'final/probe-v2.json'),'targetedFrames':len(frames),'targetedMap':rec(E/'final/targeted-frame-map.json'),'visualScope':'最终final文件两段首尾/原错误回跳点/原右侧越界点，加原尺寸42及67秒帧；上一内部fixed的67帧已检变化区间继续作中段辅助证据；狐狸中段完整镜头关系已在相同补片/上一内部合成实际输出中检查。离散帧，不是连续视听。','protected':'T14e/T17c实现与kit原SHA、AccountScene/HandoffScene调用文字逐行一致；冻结SRT/四封面SHA未变；原声AAC直接复制。','internalCorrections':'第一轮局部实际导出复核拦住提前左移跟随和补片末帧回落；已调整到原源切镜9.066667秒及eof_action=repeat+repeatlast=1+严格边界。未将内部候选交PMO。'},'limits':m['reviewLimits'],'acceptances':{'pmo':'PENDING','05':'NOT_RELEASED','user':'PENDING'},'reworkMetrics':{'pmoFindings':3,'pmoRevisionRounds':1,'internalCorrectionPasses':2,'audioReprocessing':0,'coverChanges':0,'runtimeCost':'UNKNOWN'}}
save(R/'04-定向返修自检-v2.json',qa)
# Keep v1 page as history; current entry and explicit v2 entry both point at final fixed file.
old=(R/'preview.html').read_text()
if not (R/'preview-v1.html').exists():(R/'preview-v1.html').write_text(old)
page=old.replace('· v1','· v2').replace('elden-ring-ai-recap-v1.mp4','elden-ring-ai-recap-v2-final.mp4').replace('elden-ring-ai-recap-v1.srt','elden-ring-ai-recap-v2.srt').replace('交付索引-v1.md','交付索引-v2.md')
(R/'preview-v2.html').write_text(page);(R/'preview.html').write_text(page)
print(json.dumps({'output':final,'targetedFrames':len(frames)},ensure_ascii=False))
