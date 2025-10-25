
#!/usr/bin/env bash
# Usage: ./download_youtube.sh <youtube_url> <out_dir>
URL=$1
OUT=$2
mkdir -p "$OUT"
yt-dlp -x --audio-format mp3 -o "$OUT/%(title)s.%(ext)s" "$URL"
