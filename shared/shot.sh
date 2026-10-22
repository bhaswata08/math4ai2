#!/usr/bin/env bash
# Screenshot deck slides for checking by eye.
#   shared/shot.sh <url-to-deck> <out-dir> <slide index>...
# Index N is the URL hash #/N, which reveal shows as slide N+1.
set -euo pipefail
URL="$1"; OUT="$2"; shift 2
mkdir -p "$OUT"
for i in "$@"; do
  chromium --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1400,800 --virtual-time-budget=6000 --autoplay-policy=no-user-gesture-required \
    --screenshot="$OUT/s$i.png" "$URL#/$i" 2>/dev/null >/dev/null
done
echo "wrote $# shots to $OUT"
