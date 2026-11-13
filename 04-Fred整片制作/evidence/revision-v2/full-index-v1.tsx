import React from 'react';
import {AbsoluteFill,Composition,Sequence,Img,OffthreadVideo,staticFile,useCurrentFrame,registerRoot} from 'remotion';
import {StatTriplet} from './components/T14e-StatTriplet';
import {FileTree} from './components/T17c-FileTree';
import {Fonts,textBase} from './kit/ui';
import captions from './subtitles.json';
export const AccountScene=()=> <AbsoluteFill><StatTriplet stats={[{label:'10月19日',value:26.3,decimals:1,unit:'亿 Token'},{label:'10月20日',value:24.3,decimals:1,unit:'亿 Token'},{label:'10月21日',value:18.8,decimals:1,unit:'亿 Token'},{label:'三天合计',value:69.4,decimals:1,unit:'亿 Token'}]} hero={3} cues={[.2,3.1]}/><div style={{position:'absolute',top:270,width:'100%',textAlign:'center',...textBase(64,900)}}>账号三天总量</div></AbsoluteFill>;
export const HandoffScene=()=> <AbsoluteFill><FileTree tree={[{name:'AI-Limgrave-Lab/',depth:0},{name:'game/',depth:1},{name:'LimgraveLab/',depth:2},{name:'Source/',depth:3,note:'源码'},{name:'Content/',depth:3,note:'模型资源'},{name:'assets/',depth:1},{name:'blender/',depth:2,note:'可编辑源'},{name:'export/',depth:2,note:'导出模型'}]} cues={[.18,.65,1.12,1.9,2.8,3.7,4.6]}/><div style={{position:'absolute',top:215,left:70,right:70,...textBase(90,900)}}>GitHub</div><div style={{position:'absolute',top:330,left:70,right:70,...textBase(44,600),color:'#62626a'}}>源码 + Release 资源</div></AbsoluteFill>;
const frame=(s:number)=>Math.round(s*60);
const FullVideo=({file,from=0,position='50% 50%'}:{file:string,from?:number,position?:string})=><OffthreadVideo muted src={staticFile(file)} startFrom={Math.round(from*60)} style={{width:1080,height:1920,objectFit:'cover',objectPosition:position}}/>;
const Still=({file,position='50% 50%',contain=false}:{file:string,position?:string,contain?:boolean})=><AbsoluteFill style={{background:'#111315',justifyContent:'center'}}><Img src={staticFile(file)} style={{width:1080,height:contain?1260:1920,objectFit:contain?'contain':'cover',objectPosition:position}}/></AbsoluteFill>;
const Credit=({children}:{children:React.ReactNode})=><div style={{position:'absolute',top:75,left:58,right:58,fontFamily:'Fred MiSans',fontSize:34,fontWeight:600,color:'#fff',textShadow:'0 2px 7px #000'}}>{children}</div>;
const Shot=({start,end,children}:{start:number,end:number,children:React.ReactNode})=><Sequence from={frame(start)} durationInFrames={frame(end)-frame(start)}>{children}</Sequence>;
const Prince=({from}:{from:number})=><AbsoluteFill style={{background:'#dce4df'}}><OffthreadVideo muted src={staticFile('prince-720.mp4')} startFrom={Math.round(from*60)} style={{position:'absolute',width:1080,height:1440,top:180,objectFit:'cover',objectPosition:'50% 50%'}}/><div style={{position:"absolute",top:75,left:58,right:58,fontFamily:"Fred MiSans",fontSize:34,fontWeight:600,color:"#19191c"}}>《小王子》 · Sac</div></AbsoluteFill>;
export function FullFilm(){const f=useCurrentFrame();const t=f/60;const cap=captions.find(c=>t>=c.start&&t<c.end);const light=(f>=1344&&f<1708)||(f>=4937&&f<5364)||(f>=1953&&f<2719)||(f>=3124&&f<3314)||(f>=3820&&f<4264);return <AbsoluteFill style={{background:'#111'}}><Fonts/>
 <Sequence from={0} durationInFrames={1708}><FullVideo file="talk-1.mp4"/></Sequence>
 <Sequence from={1708} durationInFrames={2556}><FullVideo file="talk-2.mp4"/></Sequence>
 <Sequence from={4264} durationInFrames={1977}><FullVideo file="talk-3.mp4"/></Sequence>
 <Shot start={10} end={12.267}><Still file="early.png" contain/><Credit>复刻过程</Credit></Shot>
 <Shot start={12.267} end={12.967}><FullVideo file="walk.mp4"/><Credit>步态测试</Credit></Shot>
 <Shot start={12.967} end={15.8}><Still file="church.png"/><Credit>我的这版</Credit></Shot>
 <Shot start={18.667} end={20.4}><Still file="tree.png"/></Shot>
 <Shot start={20.4} end={22.4}><Still file="sentinel.png"/></Shot>
 <Sequence from={1344} durationInFrames={364}><AccountScene/></Sequence>
 <Shot start={32.55} end={39.393}><Prince from={2}/></Shot>
 <Shot start={39.393} end={42.633}><Prince from={6}/></Shot>
 <Shot start={42.633} end={43.873}><Prince from={18.3}/></Shot>
 <Shot start={43.873} end={45.317}><Prince from={40}/></Shot>
 <Shot start={52.067} end={55.233}><Prince from={12}/></Shot>
 <Shot start={63.667} end={71.067}><Prince from={42}/></Shot>
 <Shot start={71.067} end={73.867}><Still file="player.png"/><Credit>我的这版</Credit></Shot>
 <Shot start={73.867} end={76.117}><Still file="died.png" contain/></Shot>
 <Sequence from={4937} durationInFrames={427}><HandoffScene/></Sequence>
 <Shot start={89.4} end={91.117}><Still file="sentinel.png"/></Shot>
 <Shot start={91.117} end={93.1}><Still file="player.png"/></Shot>
 {cap&&<div style={{position:'absolute',left:54,right:54,bottom:138,textAlign:'center',fontFamily:'Fred MiSans',fontWeight:600,fontSize:46,lineHeight:1.35,color:light?'#19191c':'#fff',textShadow:light?undefined:'0 2px 7px #000,0 2px 3px #000'}}>{cap.text}</div>}
 </AbsoluteFill>}
registerRoot(()=> <Composition id="FullFilm" component={FullFilm} width={1080} height={1920} fps={60} durationInFrames={6241}/>);
