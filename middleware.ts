import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware';
import { i18n } from '@/lib/i18n';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const i18nMiddleware = createI18nMiddleware(i18n);

export default function middleware(request: NextRequest, event: any) {
  const pathname = request.nextUrl.pathname;

  // Extract the language prefix from the pathname (/en/..., /zh/..., /ja/...)
  const lang = i18n.languages.find(
    (l) => pathname.startsWith(`/${l}/`) || pathname === `/${l}`,
  );

  if (lang) {
    // Pass the detected language to the root layout via a request header
    const headers = new Headers(request.headers);
    headers.set('x-lang', lang);
    return NextResponse.next({
      request: { headers },
    });
  }

  // No language prefix: let the i18n middleware handle redirect/rewrite
  return i18nMiddleware(request, event);
}

export const config = {
  // Matcher ignoring API routes, Next.js internals, and static assets
  // Important: exclude metadata routes like `/robots.txt` and `/sitemap.xml`
  // so they won't be redirected to `/{lang}/...` which would 404 unless you implement localized metadata routes.
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|icon.png|apple-icon.png|assets/|robots\\.txt|sitemap\\.xml|llms?\\.txt|llm-full\\.txt|llms-full\\.txt).*)',
  ],
};
