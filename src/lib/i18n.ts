import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'zh', 'ja'],
  parser: 'dir',
  // Critical for SEO: without this, missing translations fall back to the
  // default language's file system. That produced 76 fake /ja/docs/blog/* pages
  // serving English content with /ja/ URLs — Google flagged ~50 as "duplicate
  // pages" and refused to index them. With `null`, untranslated locales 404
  // (Google then drops them from the index) instead of duplicating content.
  fallbackLanguage: null,
});

export function getLocalePath(lang: string, path = ''): string {
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return cleanPath ? `/${lang}/${cleanPath}` : `/${lang}`;
}
