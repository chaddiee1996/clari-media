#!/usr/bin/env bash
# mix.sh <video.mp4> <bed.wav> <out.mp4> [vo.mp3 vo_end_seconds]
# voiced: VO loudnorm -16, bed 0.15 ducked under the voice (rising after the VO for the end card), amix normalize=0, alimiter 0.89
# text only: the bed is the star, loudnorm to -14
set -e
V=$1; B=$2; O=$3; VO=${4:-}; E=${5:-0}
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
if [ -n "$VO" ]; then
  ffmpeg -v error -y -i "$V" -i "$VO" -i "$B" -filter_complex \
  "[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo,apad[vo];[vo]asplit=2[v1][v2];\
[2:a]aresample=48000,volume='0.15+0.2*clip((t-$E)/0.9,0,1)':eval=frame[bed];\
[bed][v2]sidechaincompress=threshold=0.04:ratio=3:attack=25:release=350[bd];\
[v1][bd]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.89,atrim=0:$D[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -t "$D" -movflags +faststart "$O"
else
  ffmpeg -v error -y -i "$V" -i "$B" -filter_complex \
  "[1:a]aresample=48000,loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000,volume=-1.1dB,alimiter=limit=0.89,apad,atrim=0:$D[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -t "$D" -movflags +faststart "$O"
fi
ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate -of compact=p=0 "$O" | tr '\n' ' '; echo
