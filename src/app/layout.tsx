import type { Viewport, Metadata } from 'next';
import { GoogleAnalytics } from '@next/third-parties/google';
import { headers } from 'next/headers';
import './global.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://doc.tokenpapa.ai'),
  other: {
    charset: 'utf-8',
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: dark)', color: '#0A0A0A' },
    { media: '(prefers-color-scheme: light)', color: '#fff' },
  ],
  width: 'device-width',
  initialScale: 1,
};

const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'TokenPAPA',
  url: 'https://doc.tokenpapa.ai',
  description:
    'Unified AI API gateway providing affordable access to DeepSeek, MiniMax, and Chinese LLM APIs for overseas developers.',
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate:
        'https://doc.tokenpapa.ai/en/docs?search={search_term_string}',
    },
    'query-input': 'required name=search_term_string',
  },
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Detect language from the request header set by middleware
  const headersList = await headers();
  const lang = headersList.get('x-lang') || 'en';

  return (
    <html lang={lang} suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(websiteSchema),
          }}
        />
      </head>
      <body>
        {children}
        {process.env.NEXT_PUBLIC_GA_ID && (
          <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA_ID} />
        )}
      </body>
    </html>
  );
}
