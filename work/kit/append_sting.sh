#!/usr/bin/env bash
# Append the Clari logo sting (4 s, with the sound logo) to a finished reel.
# usage: bash append_sting.sh <reel_with_audio.mp4> <out.mp4> [crossfade seconds, default 0.4]
# The reel's own last 0.4 s cross-dissolves into the sting; the reel's audio fades under the sound logo.
set -e
IN=${1:?reel}; OUT=${2:?out}; X=${3:-0.4}
ST=/home/claude/clari-media/work/kit/sting/sting.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
OFF=$(python3 -c "print(round($D-$X,3))")
HASA=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)
if [ -z "$HASA" ]; then
  ffmpeg -v error -y -i "$IN" -f lavfi -t "$D" -i anullsrc=r=48000:cl=stereo -i "$ST" -filter_complex \
  "[0:v]fps=30,format=yuv420p,setsar=1[v0];[2:v]fps=30,format=yuv420p,setsar=1[v1];[v0][v1]xfade=transition=fade:duration=$X:offset=$OFF[v];[1:a][2:a]acrossfade=d=$X:c1=tri:c2=tri[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$IN" -i "$ST" -filter_complex \
  "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]fps=30,format=yuv420p,setsar=1[v1];[v0][v1]xfade=transition=fade:duration=$X:offset=$OFF[v];[0:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];[a0][a1]acrossfade=d=$X:c1=tri:c2=tri[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
fi
echo "done: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s)"
