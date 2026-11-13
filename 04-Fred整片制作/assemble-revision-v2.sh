#!/bin/sh
set -eu
cd "$(dirname "$0")"
# Exact frame-clock replacement, not GOP stream-copy splicing. Source AAC is copied unchanged.
/Users/USER/.local/bin/ffmpeg -n -hide_banner -i output/elden-ring-ai-recap-v1.mp4 -i output/revision-v2-cloud-fixed.mp4 -i output/revision-v2-relation.mp4 -filter_complex '[1:v]setpts=PTS-STARTPTS+1953/60/TB[c];[2:v]setpts=PTS-STARTPTS+3968/60/TB[r];[0:v][c]overlay=0:0:eof_action=repeat:repeatlast=1:enable=between(t\,32.549\,42.6323):format=auto[v1];[v1][r]overlay=0:0:eof_action=repeat:repeatlast=1:enable=between(t\,66.1323\,70.3323):format=auto[v]' -map '[v]' -map 0:a:0 -c:v libx264 -preset fast -crf 16 -pix_fmt yuvj420p -color_range pc -threads 4 -r 60 -frames:v 6241 -c:a copy -movflags +faststart output/elden-ring-ai-recap-v2-final.mp4 > evidence/revision-v2/assembly-final.log 2>&1
