port := "8013"
pidfile := "build/serve.pid"
logfile := "build/serve.log"

# Start the slide server in the background (restarts it if already running).
serve: stop
    mkdir -p build
    setsid nohup node shared/serve.mjs {{port}} > {{logfile}} 2>&1 & echo $! > {{pidfile}}
    @sleep 0.5
    @echo "serving on http://localhost:{{port}}/decks/ (pid $(cat {{pidfile}}), log {{logfile}})"

# Stop the background slide server.
stop:
    #!/usr/bin/env bash
    if [ -f {{pidfile}} ]; then kill "$(cat {{pidfile}})" 2>/dev/null; rm -f {{pidfile}}; fi
    # Fallback: whatever still holds the port.
    pid=$(ss -ltnpH "sport = :{{port}}" 2>/dev/null | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1)
    [ -n "$pid" ] && kill "$pid" && echo "killed stray pid $pid on :{{port}}" || true

# Rebuild the static site/ (every deck). Pass a deck to rebuild only its deck.html, e.g. `just build 1.1-vectors`.
build deck="":
    #!/usr/bin/env bash
    if [ -n "{{deck}}" ]; then node shared/build.mjs decks/{{deck}}; else node shared/site.mjs; fi
