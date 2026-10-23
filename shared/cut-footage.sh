#!/usr/bin/env bash
# Cut third-party footage segments into a deck's clip folder.
#
#   shared/cut-footage.sh <segments.tsv> <video-dir>
#
# segments.tsv: one segment per line, tab separated:
#   deck  name  video-file  start  end   [crop]
# e.g. decks/2.1-matrices  VKDotEngine  1.mp4  95.5  118  [w:h:x:y]
# Lines starting with # are comments. Writes <deck>/assets/clips/<name>.mp4
# (silent, h264, faststart, like render.sh) and <name>.png, the last frame.
# The source videos are not in the repo; the .tsv says where they come from.
set -euo pipefail
TSV="$1"; SRC="$2"
grep -v '^#' "$TSV" | grep -v '^\s*$' | while IFS=$'\t' read -r DECK NAME FILE START END CROP; do
    OUT="$DECK/assets/clips"; mkdir -p "$OUT"
    VF="scale=1920:1080:flags=lanczos,fps=30"
    [ -n "${CROP:-}" ] && VF="crop=$CROP,$VF"
    ffmpeg -loglevel error -y -ss "$START" -to "$END" -i "$SRC/$FILE" -vf "$VF" \
        -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart -an "$OUT/$NAME.mp4" </dev/null
    ffmpeg -loglevel error -y -sseof -0.1 -i "$OUT/$NAME.mp4" -frames:v 1 -update 1 "$OUT/$NAME.png" </dev/null
    echo "$OUT/$NAME.mp4 ($(du -h "$OUT/$NAME.mp4" | cut -f1))"
done
