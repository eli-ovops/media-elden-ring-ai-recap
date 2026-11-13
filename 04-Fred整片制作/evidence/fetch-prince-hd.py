import json,urllib.request,urllib.parse,time,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];j=json.load(open('/tmp/eli-little-prince-reference-20261023/little-prince.info.json'));f=next(x for x in j['formats'] if x['format_id']=='http-2176');u=f['url'];dest=R/'public/prince-720.mp4';r={'sourcePost':'https://x.com/Saccc_c/status/2109962425512734739','metadataFile':'/tmp/eli-little-prince-reference-20261023/little-prince.info.json','format':'http-2176','host':urllib.parse.urlsplit(u).hostname,'path':urllib.parse.urlsplit(u).path,'method':'one anonymous normal HTTPS GET; no headers/cookie/proxy changes; no retry','limits':{'bytes':30000000,'seconds':45},'status':'UNKNOWN'};start=time.monotonic()
try:
 with urllib.request.urlopen(u,timeout=12) as response:
  r['httpStatus']=response.status;buf=bytearray()
  while True:
   b=response.read(262144)
   if not b:break
   buf+=b
   if len(buf)>30000000 or time.monotonic()-start>45:raise RuntimeError('bounded-transfer-limit')
  dest.write_bytes(buf);r.update(status='DOWNLOADED',bytes=len(buf),sha256=hashlib.sha256(buf).hexdigest(),file=str(dest))
except Exception as e:r.update(status='FAILED',errorType=type(e).__name__,error=str(e) if not isinstance(e,urllib.error.HTTPError) else f'HTTP {e.code}')
r['elapsedSeconds']=round(time.monotonic()-start,3);(R/'evidence/prince-hd-transfer.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))
