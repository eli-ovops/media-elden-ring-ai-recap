// AccountScene derives the complete T14e StatTriplet and its exact wave3 kit.
import React from 'react';
import {AbsoluteFill,Composition,Sequence,Img,OffthreadVideo,staticFile,useCurrentFrame,registerRoot} from 'remotion';
import {StatTriplet} from './components/T14e-StatTriplet';
import {Fonts,textBase} from './kit/ui';
import captions from './subtitles.json';
const OFFSET=1224;
export const AccountScene=()=> <AbsoluteFill><StatTriplet stats={[{label:'10月19日',value:26.3,decimals:1,unit:'亿 Token'},{label:'10月20日',value:24.3,decimals:1,unit:'亿 Token'},{label:'10月21日',value:18.8,decimals:1,unit:'亿 Token'},{label:'三天合计',value:69.4,decimals:1,unit:'亿 Token'}]} hero={3} cues={[.2,3.1]}/><div style={{position:'absolute',top:270,width:'100%',textAlign:'center',...textBase(64,900)}}>账号三天总量</div></AbsoluteFill>;
export function Representative(){const f=useCurrentFrame();const t=(f+OFFSET)/60;const cap=captions.find(c=>t>=c.start&&t<c.end);return <AbsoluteFill style={{background:'#fff'}}><Fonts/>
  <Sequence from={0} durationInFrames={120}><Img src={staticFile('sentinel.png')} style={{width:1080,height:1920,objectFit:'cover',objectPosition:'50% 50%'}}/></Sequence>
  <Sequence from={120} durationInFrames={364}><AccountScene/></Sequence>
  <Sequence from={484} durationInFrames={245}><OffthreadVideo muted src={staticFile('talk-motivation.mp4')} style={{width:1080,height:1920,objectFit:'cover'}}/></Sequence>
  {cap&&<div style={{position:'absolute',left:54,right:54,bottom:138,textAlign:'center',fontFamily:'Fred MiSans',fontWeight:600,fontSize:46,lineHeight:1.35,color:f<120||f>=484?'white':'#19191c',textShadow:f<120||f>=484?'0 2px 7px #000,0 2px 3px #000':undefined}}>{cap.text}</div>}
 </AbsoluteFill>}
registerRoot(()=> <Composition id="Representative" component={Representative} width={1080} height={1920} fps={60} durationInFrames={729}/>);
