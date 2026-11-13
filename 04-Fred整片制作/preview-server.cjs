const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname;
http.createServer((req,res)=>{
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);return res.end();}
  let file;try{file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));}catch{res.writeHead(400);return res.end();}
  if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
  fs.stat(file,(err,s)=>{
    if(err||!s.isFile()){res.writeHead(404);return res.end();}
    const type={'.html':'text/html; charset=utf-8','.md':'text/plain; charset=utf-8','.mp4':'video/mp4','.png':'image/png','.jpg':'image/jpeg','.srt':'text/plain; charset=utf-8','.json':'application/json'}[path.extname(file)]||'application/octet-stream';
    let start=0,end=s.size-1,status=200;
    if(req.headers.range){const m=/^bytes=(\d*)-(\d*)$/.exec(req.headers.range);if(!m){res.writeHead(416,{'Content-Range':`bytes */${s.size}`});return res.end();}start=m[1]?Number(m[1]):Math.max(0,s.size-Number(m[2]));end=m[1]&&m[2]?Math.min(Number(m[2]),s.size-1):s.size-1;if(start>end||start>=s.size){res.writeHead(416,{'Content-Range':`bytes */${s.size}`});return res.end();}status=206;}
    const headers={'Content-Type':type,'Accept-Ranges':'bytes','Content-Length':end-start+1,'Cache-Control':'no-cache'};if(status===206)headers['Content-Range']=`bytes ${start}-${end}/${s.size}`;
    res.writeHead(status,headers);if(req.method==='HEAD')return res.end();const stream=fs.createReadStream(file,{start,end});stream.on('error',()=>res.destroy());res.on('close',()=>stream.destroy());stream.pipe(res);
  });
}).listen(55323,'127.0.0.1',()=>console.log('Local preview http://127.0.0.1:55323/preview.html'));
