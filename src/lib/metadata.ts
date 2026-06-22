import type { Metadata } from 'next';

export function createMetadata(override: Metadata): Metadata {
  return {
    ...override,
    // Icons are provided by the App Router file conventions
    // (src/app/icon.png, apple-icon.png, favicon.ico) so Next emits
    // content-hashed URLs that bust browser caches on rebrand.
    openGraph: {
      title: override.title ?? undefined,
      description: override.description ?? undefined,
      url: 'https://tokenpapa.ai',
      images: '/assets/logo.png',
      siteName: 'TokenPAPA',
      type: 'website',
      ...override.openGraph,
    },
    twitter: {
      card: 'summary_large_image',
      title: override.title ?? undefined,
      description: override.description ?? undefined,
      images: '/assets/logo.png',
      ...override.twitter,
    },
  };
}

export const baseUrl =
  process.env.SITE_URL
    ? new URL(process.env.SITE_URL)
    : process.env.VERCEL_PROJECT_PRODUCTION_URL
      ? new URL(`https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`)
      : new URL('http://localhost:3000');
