#!/usr/bin/env python3
"""Chuyển bộ docs NEXORA (md/mdx kiểu Docusaurus) sang nội dung Astro Starlight.

Dùng:  python3 scripts/convert-docs.py <thư mục docs gốc> [<thư mục src/content/docs>]
"""
import re, sys, posixpath
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else 'docs')
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else 'src/content/docs')
GH = 'https://github.com/withnexora/nexora/blob/main/'

# ---------- Metadata các trang tham chiếu ----------
# mode: vi | en | both | split(vi/en theo mục) | tail(vi đầy đủ + en chỉ phần English)
REF = [
 dict(src='HUONG_DAN_A_Z.md', slug='guide-a-z', mode='vi', order=1,
      t={'vi': 'Hướng dẫn triển khai & sử dụng A–Z'}, d={'vi': 'Từ clone, Supabase, admin, QR/Zalo, role, media đến GitHub, aaPanel, cPanel, static hosting và checklist production.'},
      b={'vi': ('Đầy đủ', 'success')}, chips={'vi': [('Hướng dẫn đầy đủ', 'success'), ('Tiếng Việt', 'note'), ('Phiên bản 2026-08-29', 'tip')]}),
 dict(src='DEPLOYMENT_GUIDE_EN.md', slug='deployment-guide', mode='both', order=1,
      t={'vi': 'Deployment & user guide (tiếng Anh)', 'en': 'Deployment & user guide'},
      d={'vi': 'Bản hướng dẫn triển khai và sử dụng bằng tiếng Anh: local, Supabase, hosting, role, thanh toán, email.',
         'en': 'Local setup, Supabase, GitHub Pages, static hosting, aaPanel, cPanel, roles, payments, email and troubleshooting.'},
      b={}, chips={'vi': [], 'en': []}),
 dict(src='SMTP_SETUP_BILINGUAL.md', slug='smtp-setup', mode='both', order=2,
      t={'vi': 'SMTP & email giao dịch', 'en': 'SMTP & transactional email'},
      d={'vi': 'Cài đặt SMTP hoặc Resend API, domain/DNS, biến môi trường, reset password, aaPanel, cPanel và bảo mật.',
         'en': 'Configure SMTP or the Resend API, domain/DNS, environment variables, password reset, aaPanel, cPanel and security.'},
      b={'vi': ('Song ngữ', 'note'), 'en': ('Bilingual', 'note')},
      chips={'vi': [('Email', 'tip'), ('SMTP', 'note'), ('Resend', 'success'), ('Song ngữ / Bilingual', 'note')],
             'en': [('Email', 'tip'), ('SMTP', 'note'), ('Resend', 'success'), ('Bilingual', 'note')]}),
 dict(src='PAYOS_SETUP_BILINGUAL.md', slug='payos-setup', mode='split', order=3,
      t={'vi': 'PayOS.vn — Cấu hình và vận hành', 'en': 'PayOS.vn — Setup and operations'},
      d={'vi': 'PayOS server-side, secret environment, webhook xác minh chữ ký, sandbox và xử lý sự cố.',
         'en': 'Server-side PayOS, secret environment variables, signed webhook verification, sandbox and troubleshooting.'},
      b={'vi': ('PayOS', 'tip'), 'en': ('PayOS', 'tip')},
      chips={'vi': [('Thanh toán', 'tip'), ('Webhook', 'note'), ('Sandbox', 'caution')], 'en': [('Payments', 'tip'), ('Webhook', 'note'), ('Sandbox', 'caution')]}),
 dict(src='RENDER_ENV_SETUP_BILINGUAL.md', slug='render-env', mode='tail', tail='## English checklist', order=4,
      t={'vi': 'Cấu hình Environment trên Render', 'en': 'Render environment configuration'},
      d={'vi': 'Blueprint Web Service, Build/Start command, /healthz, biến VITE_*, Supabase, PayOS và troubleshooting.',
         'en': 'Render Web Service checklist: build/start commands, health check, VITE_* variables, Supabase and PayOS.'},
      b={'vi': ('Render', 'note'), 'en': ('Render', 'note')},
      chips={'vi': [('Render', 'note'), ('Web Service', 'tip'), ('Environment', 'caution')], 'en': [('Render', 'note'), ('Web Service', 'tip'), ('Summary', 'caution')]}),
 dict(src='SUPABASE_STORAGE_SETUP.md', slug='supabase-storage', mode='tail', tail='## English summary', order=5,
      t={'vi': 'Cấu hình Supabase Storage', 'en': 'Supabase Storage setup'},
      d={'vi': 'Tạo bucket nexora-brand-assets, policy upload theo capability, kiểm thử public URL và cấu hình Render.',
         'en': 'Create the nexora-brand-assets bucket, capability-based upload policies and verify public URLs.'},
      b={'vi': ('Storage', 'note'), 'en': ('Storage', 'note')},
      chips={'vi': [('Storage', 'note'), ('Upload ảnh Admin', 'tip')], 'en': [('Storage', 'note'), ('Summary', 'caution')]}),
 dict(src='SUPABASE.md', slug='supabase-workflow', mode='vi', order=6,
      t={'vi': 'Quy trình Supabase'}, d={'vi': 'Schema canonical 25 bảng, RLS, quy trình áp dụng một lần, xác minh, checkout và cấp quyền admin an toàn.'},
      b={'vi': ('Database', 'note')}, chips={'vi': [('Database', 'note'), ('RLS', 'caution')]}),
 dict(src='ACCOUNT_WALLET.md', slug='account-wallet', mode='vi', order=7,
      t={'vi': 'Tài khoản, số dư & nạp tiền Zalo'}, d={'vi': 'Sổ cái, nạp tiền Zalo, quản trị khách, RLS và quy trình đối soát.'},
      b={'vi': ('Wallet', 'tip')}, chips={'vi': [('Wallet', 'tip'), ('Đối soát', 'caution')]}),
 dict(src='ROLE_CONTENT_AFFILIATE.md', slug='role-content-affiliate', mode='vi', order=8,
      t={'vi': 'Role, kiểm duyệt, affiliate & hoàn tiền'}, d={'vi': 'Ma trận role, moderation, article reader, referral 15%, hoàn tiền, CSV và mapping sản phẩm–gian hàng.'},
      b={'vi': ('Role', 'caution')}, chips={'vi': [('Role', 'caution'), ('Affiliate 15%', 'success'), ('Hoàn tiền', 'danger')]}),
 dict(src='FEATURE_EXPANSION_SCOPE.md', slug='feature-expansion-scope', mode='vi', order=9,
      t={'vi': 'Phạm vi mở rộng tính năng'}, d={'vi': 'Phạm vi mở rộng role, nội dung và vận hành.'},
      b={'vi': ('Scope', 'note')}, chips={'vi': [('Scope', 'note')]}),
 dict(src='MANTIS_ADMIN.md', slug='mantis-admin', mode='split', order=10,
      t={'vi': 'Mantis Admin variant', 'en': 'Mantis Admin variant'},
      d={'vi': 'Dashboard Bootstrap/Mantis riêng, dùng chung Auth/Supabase và không thay thế Command Deck.',
         'en': 'Standalone Bootstrap/Mantis dashboard sharing Auth/Supabase; does not replace the Command Deck.'},
      b={'vi': ('Variant', 'caution'), 'en': ('Variant', 'caution')},
      chips={'vi': [('Admin', 'caution'), ('Bootstrap', 'note')], 'en': [('Admin', 'caution'), ('Bootstrap', 'note')]}),
 dict(src='DEFERRED_WORK_BILINGUAL.md', slug='deferred-work', mode='split', order=11, shared_from='## Cấu trúc dữ liệu / Data model',
      t={'vi': 'Hệ thống “Ghi sau”', 'en': 'Deferred work backlog'},
      d={'vi': 'Quy ước ghi nhận yêu cầu trì hoãn, trạng thái backlog, capability deferredWork và RLS.',
         'en': 'Conventions for recording deferred requests, backlog statuses, the deferredWork capability and RLS.'},
      b={'vi': ('Backlog', 'note'), 'en': ('Backlog', 'note')},
      chips={'vi': [('Backlog', 'note'), ('RLS', 'caution')], 'en': [('Backlog', 'note'), ('RLS', 'caution')]}),
 dict(src='CK_TU_DONG_PROVIDER_NOTES.md', slug='auto-transfer-providers', mode='vi', order=12,
      t={'vi': 'CK tự động đa nhà cung cấp'}, d={'vi': 'Ghi chú kỹ thuật về chuyển khoản tự động qua nhiều nhà cung cấp.'},
      b={'vi': ('Payments', 'tip')}, chips={'vi': [('Payments', 'tip')]}),
 dict(src='MOBILE_EMAIL_VERIFICATION.md', slug='mobile-email-verification', mode='vi', order=13,
      t={'vi': 'Xác minh mobile & email URL'}, d={'vi': 'Kết quả kiểm tra mobile và liên kết email trước phát hành.'},
      b={'vi': ('QA', 'success')}, chips={'vi': [('QA', 'success'), ('Mobile', 'note')]}),
 dict(src='VERIFICATION_NOTES.md', slug='verification-notes', mode='vi', order=14,
      t={'vi': 'Ghi nhận kiểm tra giao diện'}, d={'vi': 'Ghi nhận kiểm tra Command Deck và các luồng chính trước phát hành.'},
      b={'vi': ('QA', 'success')}, chips={'vi': [('QA', 'success'), ('Command Deck', 'caution')]}),
 dict(src='LEGACY_MIGRATIONS.md', slug='legacy-migrations', mode='vi', order=15,
      t={'vi': 'Quy ước schema SQL'}, d={'vi': 'Repository chỉ giữ một schema canonical duy nhất.'},
      b={'vi': ('Legacy', 'caution')}, chips={'vi': [('Legacy', 'caution')]}),
 dict(src='Error.md', slug='known-errors', mode='both', order=16,
      t={'vi': 'Lỗi thường gặp', 'en': 'Known errors'}, d={'vi': 'Cách xử lý các lỗi nguy hiểm thường gặp.', 'en': 'How to fix common critical errors.'},
      b={'vi': ('Fix', 'danger'), 'en': ('Fix', 'danger')}, chips={'vi': [('Fix', 'danger'), ('Supabase Auth', 'note')], 'en': [('Fix', 'danger'), ('Supabase Auth', 'note')]}),
]
LOCS = {}
for r in REF:
    LOCS[r['src']] = {'vi': ['vi'], 'en': ['en']}.get(r['mode'], ['vi', 'en'])
SLUG = {r['src']: r['slug'] for r in REF}
TOPICS = ['getting-started', 'deployment', 'supabase', 'admin', 'payments', 'email-security']
TOPIC_CHIPS = {
 'getting-started': [('Node.js 20+', 'note'), ('pnpm', 'tip'), ('Supabase', 'success')],
 'deployment': [('Render', 'note'), ('aaPanel', 'note'), ('Static', 'tip'), ('Production', 'danger')],
 'supabase': [('PostgreSQL', 'note'), ('RLS', 'caution'), ('Auth', 'tip'), ('Storage', 'success')],
 'admin': [('Command Deck', 'caution'), ('Flash Sale', 'danger'), ('RBAC', 'note')],
 'payments': [('PayOS', 'tip'), ('Webhook', 'note'), ('MoMo · ZaloPay', 'success')],
 'email-security': [('SMTP', 'note'), ('Resend', 'tip'), ('SPF · DKIM · DMARC', 'danger')],
}

# ---------- Link ----------
def resolve(target, src_dir, loc):
    if re.match(r'^(https?:|mailto:|#)', target):
        return target
    path, _, anchor = target.partition('#')
    anchor = ('#' + anchor) if anchor else ''
    if path.startswith('/'):
        return None  # đường dẫn của storefront
    full = posixpath.normpath(posixpath.join(src_dir, path))
    name = posixpath.basename(full)
    if full.startswith('docs/assets/'):
        return ('/%s' % name) if name != 'README.mdx' else f'/{loc}/assets/'
    m = re.fullmatch(r'docs/(vi|en)/([\w-]+)\.mdx', full)
    if m:
        l, s = m.groups()
        return f'/{l}/' if s == 'index' else f'/{l}/{s}/' + anchor
    if full.startswith('docs/') and name in SLUG:
        av = LOCS[name]
        l = loc if loc in av else av[0]
        return (f'/{l}/reference/' if SLUG[name] == 'index' else f'/{l}/reference/{SLUG[name]}/') + anchor
    return GH + full + anchor

# ---------- MDX-safe ----------
CODE = re.compile(r'(`+)(.+?)\1')
def esc_text(s):
    s = s.replace('<br>', '\u0001').replace('<br/>', '\u0001').replace('<br />', '\u0001')
    s = re.sub(r'<(https?://[^>\s]+)>', r'[\1](\1)', s)
    s = s.replace('{', '\\{').replace('}', '\\}').replace('<', '&lt;')
    return s.replace('\u0001', '<br />')

def process_line(line, src_dir, loc):
    out, pos = [], 0
    segs = []
    for m in CODE.finditer(line):
        segs.append((False, line[pos:m.start()])); segs.append((True, m.group(0))); pos = m.end()
    segs.append((False, line[pos:]))
    res = []
    for is_code, s in segs:
        if is_code:
            res.append(s); continue
        s = re.sub(r'\[([^\]]+)\]\(/(admin[\w-]*\.html)\)', lambda m: f'{m.group(1)} (`/{m.group(2)}`)', s)
        def lk(m):
            r = resolve(m.group(2), src_dir, loc)
            return m.group(0) if r is None else f']({r})'
        s = re.sub(r'\](\()([^)\s]+)\)', lambda m: ']' + '(' + (resolve(m.group(2), src_dir, loc) or m.group(2)) + ')', s)
        res.append(esc_text(s))
    return ''.join(res)

def blockquote_kind(text):
    if re.match(r'^(\*\*)?(Không|Do not|Never|Cảnh báo|Security|Nguyên tắc bảo mật)', text) or re.match(r'^\*\*(Cảnh báo|Security|Nguyên tắc)', text):
        return 'caution'
    if re.search(r'Lộ trình|Ghi sau|Deferring', text[:40]):
        return 'tip'
    return 'note'

def convert_body(md, src_dir, loc, shift=0, strip_h1=True, topic=False):
    lines = md.split('\n')
    out, fence, i = [], None, 0
    if strip_h1:
        while lines and (not lines[0].strip() or lines[0].startswith('# ')):
            if lines[0].startswith('# '):
                lines.pop(0); break
            lines.pop(0)
    while i < len(lines):
        ln = lines[i]
        fm = re.match(r'^\s*(```+|~~~+)', ln)
        if fence:
            out.append(ln)
            if fm and fm.group(1).startswith(fence[0]) and len(fm.group(1)) >= len(fence): fence = None
            i += 1; continue
        if fm:
            fence = fm.group(1); out.append(ln); i += 1; continue
        if ln.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(re.sub(r'^>\s?', '', lines[i])); i += 1
            text = '\n'.join(q).strip()
            kind = blockquote_kind(text)
            out += [f':::{kind}', *[process_line(x, src_dir, loc) for x in q], ':::']
            continue
        h = re.match(r'^(#{2,6})\s+(.*)$', ln)
        if h and shift:
            ln = '#' * max(2, len(h.group(1)) - shift) + ' ' + h.group(2)
        out.append(process_line(ln, src_dir, loc))
        i += 1
    return '\n'.join(out).strip() + '\n'

def badges(chips):
    return '<div class="badge-row">\n' + '\n'.join(f'  <Badge text="{t}" variant="{v}" />' for t, v in chips) + '\n</div>\n'

def page(title, desc, body, chips=None, order=None, badge=None, extra_imports=''):
    fm = ['---', f'title: "{title}"', f'description: "{desc}"', '---']
    imp = "import { Steps } from '@astrojs/starlight/components';\n\n" if 'Steps' in extra_imports else ''
    return '\n'.join(fm) + '\n\n' + imp + body

def write(rel, text):
    text = re.sub(r'^(\s*)```env\b', r'\1```ini', text, flags=re.M)  # Shiki không có ngôn ngữ "env"
    p = OUT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

# ---------- Trang tham chiếu ----------
def sections(md, marker_vi='## Tiếng Việt', marker_en='## English'):
    a = md.index(marker_vi); b = md.index(marker_en)
    return md[a + len(marker_vi):b], md[b + len(marker_en):]

for r in REF:
    md = (SRC / r['src']).read_text(encoding='utf-8-sig')
    for loc in LOCS[r['src']]:
        body_md = md
        shift = 0
        if r['mode'] == 'split':
            vi, en = sections(md)
            shared = ''
            if r.get('shared_from'):
                k = md.index(r['shared_from']); en = md[md.index('## English') + 10:k]; shared = md[k:]
                vi = md[md.index('## Tiếng Việt') + 14:md.index('## English')]
            body_md = (vi if loc == 'vi' else en)
            if shared: body_md += '\n' + shared
            shift = 1 if not r.get('shared_from') else 0
            body = convert_body(body_md, 'docs', loc, shift=shift, strip_h1=False)
        elif r['mode'] == 'tail' and loc == 'en':
            i = md.index(r['tail']); tail = md[i + len(r['tail']):]
            note = f':::note\nThis is the English summary. The full step-by-step guide is written in Vietnamese: [open the full guide](/vi/reference/{r["slug"]}/).\n:::\n\n'
            body = note + convert_body(tail, 'docs', loc, strip_h1=False)
        else:
            body = convert_body(md, 'docs', loc)
        write(f'{loc}/reference/{r["slug"]}.mdx',
              page(r['t'][loc], r['d'][loc], body, None))

# ---------- 6 trang chủ đề ----------
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+')
SEC_RX = re.compile(r'^(Never|Không|Secrets? (never|không))\b')
def steps_and_asides(body, loc):
    title = 'Lưu ý bảo mật' if loc == 'vi' else 'Security note'
    out, lines, i = [], body.split('\n'), 0
    fence = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'): fence = not fence
        if not fence and re.match(r'^\d+\.\s', ln):
            blk = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]): blk.append(lines[i]); i += 1
            out += ['<Steps>', '', *blk, '', '</Steps>']; continue
        if not fence and ln and not re.match(r'^(#|\||-|\*|:::|<|```|\d+\.)', ln) and not ln.startswith(' '):
            sents = SENT_SPLIT.split(ln)
            keep = [s for s in sents if not SEC_RX.match(s)]
            warn = [s for s in sents if SEC_RX.match(s)]
            if warn:
                if keep: out.append(' '.join(keep))
                out += ['', f':::caution[{title}]', ' '.join(warn), ':::']; i += 1; continue
        out.append(ln); i += 1
    return '\n'.join(out)

for loc in ('vi', 'en'):
    for t in TOPICS:
        raw = (SRC / loc / f'{t}.mdx').read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
        fm = dict(re.findall(r'^(\w+):\s*(.*)$', m.group(1), re.M))
        body = convert_body(m.group(2), f'docs/{loc}', loc)
        body = steps_and_asides(body, loc)
        write(f'{loc}/{t}.mdx', page(fm['title'], fm['description'], body, None, extra_imports='Steps' if '<Steps>' in body else ''))

# ---------- Mục lục reference (có nhóm) ----------
GROUPS = [
 ('Hướng dẫn đầy đủ', 'Full guides', ['guide-a-z', 'deployment-guide', 'smtp-setup', 'payos-setup', 'render-env', 'supabase-storage']),
 ('Hệ thống & vận hành', 'Systems & operations', ['supabase-workflow', 'account-wallet', 'role-content-affiliate', 'mantis-admin', 'deferred-work', 'auto-transfer-providers']),
 ('Kiểm thử & ghi chú', 'QA & notes', ['mobile-email-verification', 'verification-notes', 'known-errors', 'feature-expansion-scope', 'legacy-migrations']),
]
BY = {r['slug']: r for r in REF}
for loc in ('vi', 'en'):
    vi = loc == 'vi'
    out = ['---', f'title: "{"Tài liệu tham chiếu" if vi else "Reference"}"',
           f'description: "{"Các hướng dẫn chi tiết, ghi chú kỹ thuật và kết quả kiểm thử của NEXORA." if vi else "Detailed guides, technical notes and verification results for NEXORA."}"', '---', '',
           "import { LinkCard, CardGrid } from '@astrojs/starlight/components';", '']
    out.append('Điểm bắt đầu để tra cứu mã nguồn, vận hành cửa hàng và khôi phục hạ tầng. Tài liệu được nhóm theo **mục đích sử dụng**.' if vi else 'Start here to look up the codebase, operate the store and recover infrastructure. Pages are grouped by **purpose**.')
    out.append('')
    for gv, ge, slugs in GROUPS:
        out += [f'## {gv if vi else ge}', '', '<CardGrid>']
        for s in slugs:
            r = BY[s]
            l = loc if loc in LOCS[r['src']] else LOCS[r['src']][0]
            ttl = r['t'].get(loc) or r['t'][l]
            d = r['d'].get(loc) or r['d'][l]
            if l != loc: d += ' (VI)' if l == 'vi' else ' (EN)'
            out.append(f'  <LinkCard title="{ttl}" description="{d}" href="/{loc}/reference/{s}/" />')
        out += ['</CardGrid>', '']
    out += [f'## {"Nguồn chuẩn" if vi else "Sources of truth"}', '',
            '| ' + ('Thành phần | Nguồn chuẩn' if vi else 'Component | Source') + ' |', '| --- | --- |',
            f'| Schema Supabase | [`supabase-unified.sql`]({GH}supabase-unified.sql) |',
            f'| {"Media gốc" if vi else "Original media"} | `client/public/media/` (branch `main`); [`assets/media`](https://github.com/withnexora/nexora/tree/assets/media) {"là bản backup" if vi else "is the backup"} |',
            f'| {"Mã ứng dụng và tài liệu" if vi else "App code and docs"} | {"Nhánh GitHub" if vi else "GitHub branch"} `main` |', '',
            f'## {"Tài liệu trong repository" if vi else "Repository documents"}', '',
            f'- [README]({GH}README.md) · [README (EN)]({GH}README_EN.md)',
            f'- [ADMIN_SETUP]({GH}ADMIN_SETUP.md) — {"cấp quyền Command Deck" if vi else "granting Command Deck access"}',
            f'- [ASSET_MANIFEST]({GH}ASSET_MANIFEST.md) — {"kiểm kê media và checksum" if vi else "media inventory and checksums"}',
            f'- [ideas.md]({GH}ideas.md) · [todo.md]({GH}todo.md)', '',
            ':::caution[' + ('Pháp lý' if vi else 'Legal') + ']',
            'Các trang điều khoản, bảo mật, giao hàng/đổi trả trong CMS là nội dung khởi tạo. Chủ sở hữu cần **rà soát pháp lý độc lập** trước khi công bố cho khách hàng thực.' if vi else 'The terms, privacy and shipping/returns pages in the CMS are starter content. The owner needs an **independent legal review** before publishing to real customers.',
            ':::', '']
    write(f'{loc}/reference/index.mdx', '\n'.join(out))
print('OK')
