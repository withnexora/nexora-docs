# NEXORA Docs (Astro Starlight)

Site tài liệu song ngữ **vi / en** cho NEXORA, dựng bằng [Astro Starlight](https://starlight.astro.build).

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # xuất ra ./dist
```

## Cấu trúc

| Đường dẫn | Nội dung |
| --- | --- |
| `src/content/docs/{vi,en}/` | 6 trang chủ đề + trang chủ (splash) + brand assets |
| `src/content/docs/{vi,en}/reference/` | Các guide chi tiết (từ file `.md` legacy) |
| `src/assets/` | Logo, banner, ảnh demo (Astro tự tối ưu) |
| `src/styles/custom.css` | Theme NEXORA (cyan + violet) |
| `scripts/convert-docs.py` | Chuyển lại từ thư mục `docs/` gốc sang MDX |

## Badge

- **Sidebar**: khai báo trong `astro.config.mjs` (`badge: { text, variant }`) hoặc frontmatter `sidebar.badge`.
- **Trong trang**: `<Badge text="PayOS" variant="tip" />` (variant: `note`, `tip`, `success`, `caution`, `danger`).

## Deploy

```bash
SITE_URL=https://docs.example.com npm run build
# GitHub Pages: SITE_URL=https://<user>.github.io BASE_PATH=/<repo> npm run build
```

> Link nội bộ dùng đường dẫn tuyệt đối (`/vi/...`). Nếu deploy dưới `BASE_PATH`, hãy thêm tiền tố tương ứng.

## Chuyển đổi lại từ docs gốc

```bash
python3 scripts/convert-docs.py ../docs src/content/docs
```
