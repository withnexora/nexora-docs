#!/usr/bin/env node
// Server Node (không phụ thuộc thư viện) để chạy thử/tự host:
//   ANTHROPIC_API_KEY=... GEMINI_API_KEY=... node ask-ai/server.mjs   -> http://localhost:8787  (cần ít nhất một khoá)
import { createServer } from 'node:http';
import { handleAsk, listProviders, HttpError } from './handler.mjs';

const PORT = Number(process.env.PORT || 8787);
const ORIGIN = process.env.ALLOWED_ORIGIN || '*';
const MAX_BODY = 20_000;

const server = createServer(async (req, res) => {
  const send = (status, obj) => {
    res.writeHead(status, {
      'content-type': 'application/json; charset=utf-8',
      'access-control-allow-origin': ORIGIN,
      'access-control-allow-methods': 'GET, POST, OPTIONS',
      'access-control-allow-headers': 'content-type',
    });
    res.end(obj === null ? undefined : JSON.stringify(obj));
  };
  if (req.method === 'OPTIONS') return send(204, null);
  if (req.method === 'GET' && (req.url || '').split('?')[0].endsWith('/providers')) return send(200, listProviders(process.env));
  if (req.method !== 'POST') return send(405, { error: 'Method not allowed' });
  if (ORIGIN !== '*' && req.headers.origin !== ORIGIN) return send(403, { error: 'Origin không được phép' });

  try {
    let raw = '';
    for await (const chunk of req) {
      raw += chunk;
      if (raw.length > MAX_BODY) throw new HttpError(413, 'Yêu cầu quá lớn.');
    }
    let body;
    try { body = JSON.parse(raw); } catch { throw new HttpError(400, 'JSON không hợp lệ.'); }
    const out = await handleAsk(body, process.env);
    send(200, out);
  } catch (e) {
    send(e instanceof HttpError ? e.status : 500, { error: e instanceof HttpError ? e.message : 'Lỗi máy chủ' });
  }
});
server.listen(PORT, () => console.log(`Ask AI server: http://localhost:${PORT}`));
