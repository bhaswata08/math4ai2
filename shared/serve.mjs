// Static server for editing decks.
//   node shared/serve.mjs [port]      then open http://localhost:8000/decks/<deck>/
// Serves the repo root, because decks load ../../node_modules and ../../shared.
// Supports Range requests: Chrome needs them to seek inside an mp4, and the
// clip player seeks to rewind and to park a clip on its last frame.

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import { extname, join, normalize, dirname } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const PORT = Number(process.argv[2] ?? 8000);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.mp4': 'video/mp4',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
};

createServer(async (req, res) => {
  let path = decodeURIComponent(req.url.split(/[?#]/)[0]);
  if (path.endsWith('/')) path += 'index.html';
  const file = join(ROOT, normalize(path).replace(/^(\.\.[/\\])+/, ''));
  const type = TYPES[extname(file)] ?? 'application/octet-stream';

  try {
    const info = await stat(file);
    // /decks/x without the slash: redirect, so relative paths in index.html
    // resolve inside the deck. Reading a directory as a file used to throw
    // after the 200 header had gone out and take the whole server down.
    if (info.isDirectory()) {
      res.writeHead(301, { Location: path + '/' });
      res.end();
      return;
    }
    const size = info.size;
    const range = /bytes=(\d*)-(\d*)/.exec(req.headers.range ?? '');
    if (range) {
      const start = range[1] ? Number(range[1]) : 0;
      const end = Math.min(range[2] ? Number(range[2]) : size - 1, size - 1);
      if (start > end) {
        res.writeHead(416, { 'Content-Range': `bytes */${size}` });
        res.end();
        return;
      }
      res.writeHead(206, {
        'Content-Type': type,
        'Content-Range': `bytes ${start}-${end}/${size}`,
        'Content-Length': end - start + 1,
        'Accept-Ranges': 'bytes',
      });
      createReadStream(file, { start, end }).on('error', () => res.destroy()).pipe(res);
      return;
    }
    res.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' });
    res.end(await readFile(file));
  } catch {
    if (res.headersSent) { res.destroy(); return; }
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('not found');
  }
}).listen(PORT, () => {
  console.log(`serving ${ROOT} at http://localhost:${PORT}/decks/<deck>/`);
});
