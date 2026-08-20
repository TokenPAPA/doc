import { docs } from '@/.source';
import { type InferPageType, loader } from 'fumadocs-core/source';
import { lucideIconsPlugin } from 'fumadocs-core/source/lucide-icons';
import { openapiPlugin } from 'fumadocs-openapi/server';
import { i18n } from '@/lib/i18n';

export const source = loader({
  baseUrl: '/docs',
  i18n,
  source: docs.toFumadocsSource(),
  plugins: [
    lucideIconsPlugin(),
    openapiPlugin(), // Add badges to API pages in the page tree
  ],
});

export function getPageImage(page: InferPageType<typeof source>) {
  const segments = [...page.slugs, 'image.png'];

  return {
    segments,
    url: `/og/docs/${segments.join('/')}`,
  };
}

export async function getLLMText(page: InferPageType<typeof source>) {
  const processed = await page.data.getText('processed');

  // MDX image processing leaves {__imgN} placeholders in the extracted
  // text. Googlebot treats them as URLs (/zh/llms.mdx/apps/{__img0}),
  // generating 404 crawl errors, so strip them out.
  const cleaned = processed.replace(/\{__img\d+\}/g, '');

  return `# ${page.data.title}

${cleaned}`;
}
