# elden-ring-ai-recap-20261023 · 04完整工程

从[交付索引](交付索引-v1.md)进入当前结果。主入口`src/full-index.tsx`，合成`FullFilm`，6241帧/60fps/1080×1920。`src/index.tsx`和representative输出属于已验代表片段，保留追溯。

工程包含当前完整源码、实际媒体、字体、字幕、封面、Manifest与检查证据。`node_modules`复用本机已有依赖符号链接，非自包含安装包；实际版本和链接目的地见`evidence/runtime-dependencies.json`。Remotion/renderer/bundler4.0.451，React19.2.5。本机Chrome为渲染器。付费Fred库保持既有位置，不整体打包分发。

## 本地预览

在工程目录运行`node preview-server.cjs`，仅绑定127.0.0.1:55323。打开 http://127.0.0.1:55323/preview.html 。已运行时直接复用，不重复占用端口。

## 重导出

当前完整成片已经存在，不需要重复渲染。需要另改版本时先定新输出文件名并保护本版，`render-full.cjs`当前默认写`output/full-picture-v1.mp4`，不可盲目运行覆盖现有结果。

制作逻辑：`node render-full.cjs`渲染静音画面，然后使用既有FFmpeg将冻结`public/voice.wav`按1倍速/0dB合成单AAC音轨，视频流直接复制，时长104.0166666667秒，开启faststart。等价合成参数如下；`-n`用于防止覆盖既有文件，改版时选新的输出名：

```sh
/Users/USER/.local/bin/ffmpeg -n -i output/full-picture-v1.mp4 -i public/voice.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -ac 1 -t 104.0166666667 -movflags +faststart output/elden-ring-ai-recap-v1.mp4
```

`prepare.py`与`record-full-gates.py`是本次阶段脚本，可能覆盖计划/Manifest；不要在续接时盲跑。`finalize-delivery.py`刷新本期输出绑定和检查索引；它不渲染视频、不自动产生视觉验收，脚本记录必须有实际检查支撑。

实际门禁运行文件为`evidence/Manifest-final-suggestion.json`和`Manifest-final-keyframes.json`；对应`gate-final-*.json`记录PASS。主Manifest与keyframes快照同版。原预览/源码/kit/调用/实际导出链在各页referenceChoices、keyframeReview中。

声画检查边界见`04-完整成片自检-v1.json`，直接听音及正常速度连续声画仍UNKNOWN。整片PMO/05/用户认可待后续独立记录。
