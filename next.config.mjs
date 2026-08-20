import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    serverActions: {
      allowedOrigins: [
        'localhost:3000',
        // newapi.pro domains
        'docs.newapi.pro',
        'newapi.pro',
        'www.newapi.pro',
        // tokenpapa.ai domains
        'doc.tokenpapa.ai',
        'tokenpapa.ai',
        'www.tokenpapa.ai',
        // newapi.ai domains
        'docs.newapi.ai',
        'newapi.ai',
        'www.newapi.ai',
        // Vercel preview
        'new-api-docs-v1.vercel.app',
      ],
    },
  },
  async headers() {
    return [
      {
        // Apply charset to HTML pages
        source: '/:lang(en|zh|ja)/:path*',
        headers: [
          {
            key: 'Content-Type',
            value: 'text/html; charset=utf-8',
          },
        ],
      },
      {
        // OG image route handlers must serve real PNGs; the generic
        // language-scoped rule above forces text/html, so this rule
        // must come AFTER it to override the header.
        source: '/:lang(en|zh|ja)/og/:path*',
        headers: [
          {
            key: 'Content-Type',
            value: 'image/png',
          },
        ],
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: '/:lang/docs/:path*.mdx',
        destination: '/:lang/llms.mdx/:path*',
      },
    ];
  },
};

export default withMDX(config);
