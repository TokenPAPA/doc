import { generateLLMsText } from '@/lib/llms';
import { i18n } from '@/lib/i18n';
import { baseUrl } from '@/lib/metadata';

export const revalidate = false;

export async function GET() {
  return new Response(generateLLMsText(baseUrl.origin, i18n.defaultLanguage), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}
