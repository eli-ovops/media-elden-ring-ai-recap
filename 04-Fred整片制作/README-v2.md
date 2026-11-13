# v2当前工程

从[交付索引-v2](交付索引-v2.md)进入，当前完整视频是`output/elden-ring-ai-recap-v2-final.mp4`。主Manifest为`Manifest-v2.json`，`Manifest.json`与其相同；`Manifest-v1.json`冻结上版，历史门禁不升级为本版新增验收。

主源码仍`src/full-index.tsx`；只增加Prince实际媒体的跟随取景、连续时钟及狐狸镜头宽取景。T14e/T17c组件、kit、字幕与四封面未改。原声从v1成片AAC直接复制。

本次生成链：准确源媒体 → 当前FullFilm → 局部渲染cloud-fixed帧1953–2557及relation帧3968–4219 → `assemble-revision-v2.sh`精确时间轴覆盖 → 当前完整MP4。补片时钟与首尾只以整数帧为准。合成使用`eof_action=repeat:repeatlast=1`配合明确退出边界，避免补片EOF提早露出旧画面。

`render-revision-v2.cjs`当前只重建最后修正的cloud-fixed；relation原补片沿用。完整重建入口为`render-full-v2.cjs`，输出单独`output/full-picture-v2.mp4`，仅在确需重新导出时使用；现成完整v2无需重渲。重导出后画面配原声可用已装FFmpeg，视频流复制、音轨从v1直接复制，输出新的文件名并用`-n`保护现有结果。

本地页面启动仍是`node preview-server.cjs`，仅127.0.0.1:55323，当前入口`preview-v2.html`，通用`preview.html`也指向本版，旧页`preview-v1.html`保留。

依赖仍为已有Remotion4.0.451/React19.2.5本机符号链接，准确路径见`evidence/runtime-dependencies.json`；不是自包含安装包。源码及媒体完整留本工程，不另外公开分发付费库。

检查只覆盖本轮变化及接缝，详见`04-定向返修自检-v2.json`。根目录原`README.md`为v1制作历史入口；v2以本页为准。不要盲跑旧prepare/finalize脚本覆盖当前Manifest。
