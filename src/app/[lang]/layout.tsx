import { defineI18nUI } from 'fumadocs-ui/i18n';
import { i18n } from '@/lib/i18n';
import { Provider } from '@/components/provider';
import '../global.css';
import type { Metadata } from 'next';
import { createMetadata, baseUrl } from '@/lib/metadata';
import { notFound } from 'next/navigation';

const { provider } = defineI18nUI(i18n, {
  translations: {
    en: {
      displayName: 'English',
    },
    zh: {
      displayName: '简体中文',
      search: '搜索文档',
      searchNoResult: '没有结果',
      toc: '目录',
      lastUpdate: '最后更新于',
      chooseTheme: '选择主题',
      chooseLanguage: '选择语言',
      nextPage: '下一页',
      previousPage: '上一页',
      tocNoHeadings: '目录为空',
    },
    ja: {
      displayName: '日本語',
      search: 'ドキュメントを検索',
      searchNoResult: '結果が見つかりません',
      toc: '目次',
      lastUpdate: '最終更新',
      chooseTheme: 'テーマを選択',
      chooseLanguage: '言語を選択',
      nextPage: '次のページ',
      previousPage: '前のページ',
      tocNoHeadings: '見出しがありません',
    },
  },
});

const titleMap: Record<
  string,
  { default: string; template: string; description: string }
> = {
  en: {
    default: 'TokenPAPA - The Foundation of Your AI Universe',
    template: '%s | TokenPAPA',
    description:
      'Connect all AI providers, manage your AI assets, and build the future on a unified infrastructure platform. Deploy in minutes, scale effortlessly.',
  },
  zh: {
    default: 'TokenPAPA - AI 基座',
    template: '%s | TokenPAPA',
    description:
      '承载所有 AI 应用，管理你的数字资产，连接未来的统一基础设施平台。快速部署，轻松扩展。',
  },
  ja: {
    default: 'TokenPAPA - あなたの AI ユニバースの基盤',
    template: '%s | TokenPAPA',
    description:
      'すべての AI プロバイダーを接続し、AI アセットを管理し、統一されたインフラストラクチャプラットフォームで未来を構築。数分でデプロイ、簡単にスケール。',
  },
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string }>;
}): Promise<Metadata> {
  const lang = (await params).lang;
  const titles = titleMap[lang] || titleMap.en;

  return createMetadata({
    metadataBase: baseUrl,
    title: {
      default: titles.default,
      template: titles.template,
    },
    description: titles.description,
    keywords: [
      'AI Infrastructure',
      'AI Gateway',
      'AI Asset Management',
      'API Orchestration',
      'AI Application Platform',
      'Multi-Model Integration',
      'Enterprise AI',
      'AI Ecosystem',
      'Unified AI Interface',
      'Intelligent API Management',
    ],
    authors: [
      { name: 'TokenPAPA Team', url: 'https://github.com/TokenPAPA/doc' },
    ],
    creator: 'TokenPAPA Team',
    alternates: {
      languages: {
        en: '/en',
        zh: '/zh',
        ja: '/ja',
      },
    },
    openGraph: {
      type: 'website',
      locale: lang,
      title: titles.default,
      description: titles.description,
      siteName: 'TokenPAPA',
    },
    twitter: {
      card: 'summary_large_image',
      title: titles.default,
      description: titles.description,
    },
  });
}

export async function generateStaticParams() {
  return i18n.languages.map((lang) => ({ lang }));
}

export default async function RootLayout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  // Check if the language is valid, prevent invalid language codes (e.g. 'api') from causing errors
  if (!i18n.languages.includes(lang as (typeof i18n.languages)[number])) {
    notFound();
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Organization',
            name: 'TokenPAPA',
            url: 'https://doc.tokenpapa.ai',
            logo: 'https://doc.tokenpapa.ai/assets/tokenpapa.png',
            description:
              'Unified AI API gateway providing affordable access to DeepSeek, MiniMax, and Chinese LLM APIs for overseas developers.',
            sameAs: [
              'https://tokenpapa.ai',
              'https://github.com/TokenPAPA/doc',
            ],
            contactPoint: {
              '@type': 'ContactPoint',
              url: 'https://tokenpapa.ai',
              contactType: 'sales',
            },
            address: {
              '@type': 'PostalAddress',
              addressCountry: 'US',
            },
          }),
        }}
      />
      <Provider i18n={provider(lang)} lang={lang}>
        {children}
      </Provider>
    </>
  );
}
