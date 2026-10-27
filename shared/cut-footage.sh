#!/usr/bin/env bash
# Cut third-party footage segments into a deck's clip folder.
#
#   shared/cut-footage.sh <segments.tsv> <video-dir>
#
# segments.tsv: one segment per line, tab separated:
#   deck  name  video-file  start  end   [crop]  [card-grey]
# e.g. decks/2.1-matrices  VKDotEngine  1.mp4  95.5  118  [w:h:x:y]
# crop is w:h:x:y, or - for none. card-grey is the level (0-255) of a flat
# neutral grey card behind the panels; it becomes the floor of the lift below
# in place of 8, so the card disappears into the slide background like the
# near-black of the other videos.
# Lines starting with # are comments. Writes <deck>/assets/clips/<name>.mp4
# (silent, h264, faststart, like render.sh) and <name>.png, the last frame.
# The source videos are not in the repo; the .tsv says where they come from.
set -euo pipefail
TSV="$1"; SRC="$2"
# The source videos sit on near-black (about rgb 8,8,8); the slides on #12151b.
# Lift that floor to the slide background so a clip has no visible box, and
# stretch the rest of the range so whites stay white.
lift() {  # $1 = floor level
    local f="$1" n=$((255 - $1))
    echo "format=rgb24,lutrgb=r='18+max(val-$f\\,0)*237/$n':g='21+max(val-$f\\,0)*234/$n':b='27+max(val-$f\\,0)*228/$n',format=yuv420p"
}
grep -v '^#' "$TSV" | grep -v '^\s*$' | while IFS=$'\t' read -r DECK NAME FILE START END CROP GREY; do
    OUT="$DECK/assets/clips"; mkdir -p "$OUT"
    VF="scale=1920:1080:flags=lanczos,fps=30,$(lift "${GREY:-8}")"
    [ -n "${CROP:-}" ] && [ "$CROP" != "-" ] && VF="crop=$CROP,$VF"
    ffmpeg -loglevel error -y -ss "$START" -to "$END" -i "$SRC/$FILE" -vf "$VF" \
        -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart -an "$OUT/$NAME.mp4" </dev/null
    ffmpeg -loglevel error -y -sseof -0.1 -i "$OUT/$NAME.mp4" -frames:v 1 -update 1 "$OUT/$NAME.png" </dev/null
    echo "$OUT/$NAME.mp4 ($(du -h "$OUT/$NAME.mp4" | cut -f1))"
done
