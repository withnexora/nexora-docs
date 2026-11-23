# NEXORA Docs (Astro Starlight)

Bilingual documentation site **vi / en** for NEXORA, built with [Astro Starlight](https://starlight.astro.build).

```bash
npm install
npm run dev # http://localhost:4321
npm run build # output ./dist
```

## Structure

| Path | Content |
| --- | --- |
| `src/content/docs/{en,en}/` | 6 theme pages + home page (splash) + brand assets |
| `src/content/docs/{vi,en}/reference/` | Detailed guides (from legacy `.md` file) |
| `src/assets/` | Logo, banner, demo image (Astro self-optimizes) |
| `src/styles/custom.css` | Theme NEXORA (cyan + violet) |
| `scripts/convert-docs.py` | Switch back from the original `docs/` directory to MDX |

## Badges

- **Sidebar**: declared in `astro.config.mjs` (`badge: { text, variant }`) or frontmatter `sidebar.badge`.
- **In page**: `<Badge text="PayOS" variant="tip" />` (variant: `note`, `tip`, `success`, `caution`, `danger`).

## Deploy

```bash
SITE_URL=https://docs.example.com npm run build
# GitHub Pages: SITE_URL=https://<user>.github.io BASE_PATH=/<repo> npm run build
```

> Internal links use absolute paths (`/vi/...`). If deploying under `BASE_PATH`, add the corresponding prefix.

## Convert back from original docs

```bash
python3 scripts/convert-docs.py ../docs src/content/docs
```

## Ask AI (robot button next to search bar)

The **Ask AI** button (or `Ctrl+J`) opens the chat panel. There are two modes:

1. **Default (no configuration required):** looks up documents using the Pagefind index and returns relevant pages with snippets. Needs `npm run build` to get index.
2. **Answer by AI:** the panel sends questions and found documents to your Ask AI server (`ask-ai/`). Server supports **Claude** and **Gemini**; Any model that has a key will be enabled. If enabled from 2 models, the panel displays a check box (Claude / Gemini), remember to select and label the model under each answer. The API key resides only on the server, never on the frontend.

### Test run locally

```bash
ANTHROPIC_API_KEY=sk-ant-... GEMINI_API_KEY=... npm run ask-ai # http://localhost:8787 (set one or both keys)
PUBLIC_AI_ENDPOINT=http://localhost:8787 npm run build && npm run preview
```

### Deploy to Cloudflare Workers

```bash
cd ask-ai
npx wrangler secret put ANTHROPIC_API_KEY # and/or
npx wrangler secret put GEMINI_API_KEY
# edit ALLOWED_ORIGIN in wrangler.toml to your docs site domain
npx wrangler deploy
```

Then build the site with `PUBLIC_AI_ENDPOINT=https://<worker>.workers.dev`.

- Default models: `claude-sonnet-5-5` and `gemini-2.5-flash` (changed to `ANTHROPIC_MODEL` / `GEMINI_MODEL`; please check if the model name is valid for your account). `AI_PROVIDER` sets the default model when not selected by the user.
- API: `GET /providers` → `{ providers, default }`; `POST { question, lang, provider?, sources: [{ title, url, excerpt }] }` → `{ answer, provider }`.
- Limit: question 500 characters, 4 sources, request 20 KB. The source content is escaped and treated as data, not instructions. The Gemini key is sent via the `x-goog-api-key` header, not in the URL.
- Before opening publicly, set `ALLOWED_ORIGIN` and add rate limiting (e.g. Cloudflare Rate Limiting): each question costs the API.

## Interface

- Light / Dark: round button in header, save selection in `localStorage` (`starlight-theme`).
- Liquid glass optimized version: rounded header/sidebar, liquid background with gradient moving through `transform`. Real blur is only used in headers and dialog boxes (search, Ask AI); The remaining blocks use a semi-transparent background + light border so the scrolling is still smooth. Theme is located in `src/styles/custom.css`; the effect turns itself off when "reduce motion/transparency" is enabled.
- Performance: background only moves when stationary (pauses while scrolling); Devices with ≤4 cores/≤4 GB of RAM use **light mode** (no blur, no motion). Force the mode with `localStorage.setItem('nx-fx', 'lite' | 'full')` then reload the page.