import { redirect } from 'next/navigation';
import { getLocalePath, i18n } from '@/lib/i18n';

/**
 * The marketing landing page was removed. Visiting a locale root sends the
 * visitor straight into the user guide.
 */
export default async function Page({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  redirect(getLocalePath(lang, 'docs/guide/feature-guide/user/auth'));
}

export function generateStaticParams() {
  return i18n.languages.map((lang) => ({ lang }));
}
