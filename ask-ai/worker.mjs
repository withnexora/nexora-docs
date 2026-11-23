// Cloudflare Worker: wrangler secret put ANTHROPIC_API_KEY (và/hoặc GEMINI_API_KEY) && wrangler deploy
import { handleAsk, listProviders, HttpError } from './handler.mjs';

const MAX_BODY = 20_000;

export default {
  async fetch(request, env) {
    const origin = env.ALLOWED_ORIGIN || '*';
    const cors = {
      'access-control-allow-origin': origin,
      'access-control-allow-methods': 'GET, POST, OPTIONS',
      'access-control-allow-headers': 'content-type',
      'access-control-max-age': '86400',
      vary: 'origin',
    };
    const json = (obj, status = 200) =>
      new Response(JSON.stringify(obj), { status, headers: { ...cors, 'content-type': 'application/json; charset=utf-8' } });

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method === 'GET' && new URL(request.url).pathname.endsWith('/providers')) return json(listProviders(env));
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
    if (origin !== '*' && request.headers.get('origin') !== origin) return json({ error: 'Origin không được phép' }, 403);

    try {
      const raw = await request.text();
      if (raw.length > MAX_BODY) throw new HttpError(413, 'Yêu cầu quá lớn.');
      let body;
      try { body = JSON.parse(raw); } catch { throw new HttpError(400, 'JSON không hợp lệ.'); }
      const out = await handleAsk(body, env);
      return json(out);
    } catch (e) {
      return json({ error: e instanceof HttpError ? e.message : 'Lỗi máy chủ' }, e instanceof HttpError ? e.status : 500);
    }
  },
};
