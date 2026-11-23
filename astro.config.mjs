// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Đặt SITE / BASE khi deploy (vd. GitHub Pages: base: '/tech-ecommerce-store')
const site = process.env.SITE_URL || undefined;
const base = process.env.BASE_PATH || undefined;

export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: { vi: 'Tài liệu NEXORA', en: 'NEXORA Docs' },
      description: 'Tài liệu cài đặt, vận hành và phát triển nền tảng thương mại công nghệ NEXORA.',
      logo: { src: './src/assets/nexora-logo.png', alt: 'NEXORA' },
      favicon: '/favicon.png',
      defaultLocale: 'vi',
      locales: {
        vi: { label: 'Tiếng Việt', lang: 'vi' },
        en: { label: 'English', lang: 'en' },
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/withnexora/nexora',
        },
      ],
      editLink: {
        baseUrl: 'https://github.com/withnexora/nexora-docs/edit/main/',
      },
      lastUpdated: true,
      head: [
        {
          // Tự chọn chế độ nhẹ cho máy yếu (đặt trước khi vẽ để tránh nháy)
          tag: 'script',
          content:
            "(function(){try{var d=document.documentElement,l=localStorage.getItem('nx-fx');var low=(navigator.hardwareConcurrency||8)<=4||(navigator.deviceMemory||8)<=4||matchMedia('(prefers-reduced-data: reduce)').matches;if(l==='lite'||(l!=='full'&&low))d.dataset.fx='lite'}catch(e){}})()",
        },
        {
          // Tạm dừng animation nền khi đang cuộn
          tag: 'script',
          content:
            "(function(){var t,d=document.documentElement;addEventListener('scroll',function(){d.classList.add('is-scrolling');clearTimeout(t);t=setTimeout(function(){d.classList.remove('is-scrolling')},160)},{passive:true})})()",
        },
      ],
      customCss: ['./src/styles/custom.css'],
      components: {
        ThemeSelect: './src/components/ThemeToggle.astro',
        Search: './src/components/SearchWithAI.astro',
      },
      sidebar: [
        {
          label: 'Bắt đầu',
          translations: { en: 'Start here' },
          items: [
            { slug: 'getting-started', label: 'Bắt đầu nhanh', translations: { en: 'Getting started' } },
            { slug: 'deployment', label: 'Triển khai', translations: { en: 'Deployment' } },
            { slug: 'supabase', label: 'Supabase' },
          ],
        },
        {
          label: 'Vận hành',
          translations: { en: 'Operations' },
          items: [
            { slug: 'admin', label: 'Admin & Command Deck', translations: { en: 'Admin & Command Deck' } },
            { slug: 'payments', label: 'Thanh toán', translations: { en: 'Payments' } },
            { slug: 'email-security', label: 'Email & bảo mật', translations: { en: 'Email & security' } },
          ],
        },
        {
          label: 'Tài liệu tham chiếu',
          translations: { en: 'Reference' },
          items: [
            { slug: 'reference', label: 'Tổng quan', translations: { en: 'Overview' } },
            {
              label: 'Hướng dẫn đầy đủ',
              translations: { en: 'Full guides' },
              collapsed: true,
              items: [
                { slug: 'reference/full-guide', label: 'Hướng dẫn A–Z', translations: { en: 'Deployment guide' } },
                { slug: 'reference/smtp-setup', label: 'SMTP & email', translations: { en: 'SMTP & email' } },
                { slug: 'reference/payos-setup', label: 'PayOS', translations: { en: 'PayOS' } },
                { slug: 'reference/render-env', label: 'Render environment', translations: { en: 'Render environment' } },
                { slug: 'reference/supabase-storage', label: 'Supabase Storage', translations: { en: 'Supabase Storage' } },
              ],
            },
            {
              label: 'Hệ thống & vận hành',
              translations: { en: 'Systems & operations' },
              collapsed: true,
              items: [
                { slug: 'reference/supabase-workflow', label: 'Quy trình Supabase', translations: { en: 'Supabase workflow' } },
                { slug: 'reference/account-wallet', label: 'Tài khoản & ví', translations: { en: 'Account & wallet' } },
                { slug: 'reference/role-content-affiliate', label: 'Role & affiliate', translations: { en: 'Roles & affiliate' } },
                { slug: 'reference/mantis-admin', label: 'Mantis Admin', translations: { en: 'Mantis Admin' } },
                { slug: 'reference/deferred-work', label: 'Ghi sau (backlog)', translations: { en: 'Deferred work' } },
                { slug: 'reference/auto-transfer-providers', label: 'CK tự động', translations: { en: 'Auto transfer providers' } },
              ],
            },
            {
              label: 'Kiểm thử & ghi chú',
              translations: { en: 'QA & notes' },
              collapsed: true,
              items: [
                { slug: 'reference/mobile-email-verification', label: 'Mobile & email URL', translations: { en: 'Mobile & email URL' } },
                { slug: 'reference/verification-notes', label: 'Kiểm tra giao diện', translations: { en: 'UI verification' } },
                { slug: 'reference/known-errors', label: 'Lỗi thường gặp', translations: { en: 'Known errors' } },
                { slug: 'reference/feature-expansion-scope', label: 'Phạm vi mở rộng', translations: { en: 'Feature scope' } },
                { slug: 'reference/legacy-migrations', label: 'Quy ước schema SQL', translations: { en: 'SQL schema policy' } },
              ],
            },
          ],
        },
        {
          label: 'Tài sản thương hiệu',
          translations: { en: 'Brand assets' },
          items: [
            { slug: 'assets', label: 'Logo & banner', translations: { en: 'Logos & banners' } },
          ],
        },
      ],
    }),
  ],
});
