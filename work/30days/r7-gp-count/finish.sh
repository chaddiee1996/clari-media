#!/usr/bin/env bash
# usage: finish.sh <reel dir> "<final name without .mp4>"
set -e
R=$1; NAME=$2; cd "$R"
ffmpeg -v error -y -i out/picture.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest out/mixed.mp4
bash /home/claude/clari-media/work/kit/append_sting.sh out/mixed.mp4 out/final.mp4
python3 /home/claude/clari-media/.claude/skills/claude-video-studio/scripts/pacing_check.py out/final.mp4 --end-hold 4.5 | tail -8
cp out/final.mp4 "/home/claude/clari/30 days/$NAME.mp4"
