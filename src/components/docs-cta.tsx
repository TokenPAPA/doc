import { cn } from '@/lib/cn';
import { buttonVariants } from '@/components/ui/button';

/**
 * End-of-page call to action for docs pages.
 *
 * Rationale: the 68 non-blog docs pages (API reference, guides, apps) had
 * ZERO links back to the main site's conversion pages (/pricing, /register),
 * so visitors arriving from search had no path to sign up. This adds one
 * consistent CTA at the bottom of every docs page.
 *
 * Blog articles are excluded (see the docs page template) because they
 * already end with an in-content "Get Started" CTA — stacking a second one
 * there reads as spam.
 */

const translations = {
  en: {
    title: 'Ready to build?',
    desc: 'One OpenAI-compatible API key for all 67 models. No Chinese phone number required.',
    primary: 'Get your API key',
    secondary: 'See live pricing →',
  },
  zh: {
    title: '准备好开始了吗？',
    desc: '一个 OpenAI 兼容的 API Key，覆盖全部 67 个模型，无需中国手机号。',
    primary: '获取 API Key',
    secondary: '查看实时定价 →',
  },
  ja: {
    title: 'さっそく始めましょう',
    desc: '67 モデルすべてを 1 つの OpenAI 互換 API キーで。中国の電話番号は不要です。',
    primary: 'APIキーを取得',
    secondary: '料金を見る →',
  },
};

export interface DocsCtaProps {
  lang: string;
  /** Page slug used for UTM attribution, e.g. `api/ai-model/chat/openai`. */
  slug: string;
}

export function DocsCta({ lang, slug }: DocsCtaProps) {
  const t = translations[lang as keyof typeof translations] ?? translations.en;
  const utm = `utm_source=docs&utm_medium=cta&utm_campaign=${encodeURIComponent(slug)}`;

  return (
    <aside className="not-prose mt-10 flex flex-col gap-4 rounded-xl border bg-fd-card p-5 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-base font-semibold">{t.title}</p>
        <p className="mt-1 text-sm text-fd-muted-foreground">{t.desc}</p>
      </div>
      <div className="flex shrink-0 flex-wrap items-center gap-3">
        <a
          href={`https://tokenpapa.ai/register?${utm}`}
          target="_blank"
          rel="noreferrer noopener"
          className={cn(buttonVariants({ color: 'primary' }), 'px-4 py-2')}
        >
          {t.primary}
        </a>
        <a
          href={`https://tokenpapa.ai/pricing?${utm}`}
          target="_blank"
          rel="noreferrer noopener"
          className={cn(buttonVariants({ color: 'outline' }), 'px-4 py-2')}
        >
          {t.secondary}
        </a>
      </div>
    </aside>
  );
}
