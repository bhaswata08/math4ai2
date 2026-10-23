#!/usr/bin/env bash
# Render one manim scene into a deck's clip folder.
#
#   shared/anim/render.sh anim/1.1-vectors/addition.py VectorAddition decks/1.1-vectors [-qh|-ql]
#
# Writes decks/<deck>/assets/clips/<Scene>.mp4 and a poster frame
# <Scene>.png (the last frame, which is what the slide shows before the clip
# plays and after it ends). Use -ql for a fast draft while iterating; drafts
# are written to build/drafts/<deck>/ instead.
# manim comes from the pinned flake in this repo, see flake.nix.
set -euo pipefail

SRC="$1"; SCENE="$2"; DECK="$3"; QUALITY="${4:--qh}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MEDIA="$ROOT/build/manim"
# Only a full-quality render lands in the deck. Drafts go to build/drafts so
# they can never overwrite a finished 1080p clip.
if [ "$QUALITY" = "-qh" ]; then
    OUT="$ROOT/$DECK/assets/clips"
else
    OUT="$ROOT/build/drafts/$DECK"
fi
mkdir -p "$OUT"

PYTHONPATH="$ROOT" nix run "$ROOT#manim" -- render "$QUALITY" --format=mp4 \
    --media_dir "$MEDIA" "$ROOT/$SRC" "$SCENE"

case "$QUALITY" in
    -ql) HEIGHT=480 ;;
    -qm) HEIGHT=720 ;;
    -qh) HEIGHT=1080 ;;
    *) echo "unsupported quality $QUALITY" >&2; exit 1 ;;
esac
# manim names the folder <height>p<fps>. house.py pins 30 fps, which turns
# the -ql default of 480p15 into 480p30, so match the height only.
RAW="$(ls -t "$MEDIA/videos/$(basename "$SRC" .py)/${HEIGHT}p"*/"$SCENE.mp4" | head -1)"

# Re-encode small and seekable: h264, yuv420p for every browser, faststart
# so playback begins before the whole file is read.
ffmpeg -loglevel error -y -i "$RAW" -c:v libx264 -preset slow -crf 24 \
    -pix_fmt yuv420p -movflags +faststart -an "$OUT/$SCENE.mp4"
ffmpeg -loglevel error -y -sseof -0.1 -i "$OUT/$SCENE.mp4" -frames:v 1 -update 1 "$OUT/$SCENE.png"
echo "$OUT/$SCENE.mp4 ($(du -h "$OUT/$SCENE.mp4" | cut -f1))"
