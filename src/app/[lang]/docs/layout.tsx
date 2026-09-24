import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions, linkItems, getPromoTabs } from '@/lib/layout.shared';
import { getSidebarTabs } from 'fumadocs-ui/utils/get-sidebar-tabs';
import { BackToHome } from '@/components/back-to-home';
// AI feature temporarily disabled
// import { AISearchTrigger } from '@/components/search';
import 'katex/dist/katex.min.css';
import { notFound } from 'next/navigation';
import { i18n } from '@/lib/i18n';

export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const { lang } = await params;

  // Check if the language is valid, prevent invalid language codes (e.g. 'api') from causing errors
  if (!i18n.languages.includes(lang as (typeof i18n.languages)[number])) {
    notFound();
  }

  const base = baseOptions(lang);

  return (
    <DocsLayout
      {...base}
      tabMode="top"
      tree={source.pageTree[lang]}
      links={linkItems}
      sidebar={{
        defaultOpenLevel: 0,
        // Auto-derived section tabs (User Guide / API Reference / ...) plus the
        // main site's conversion entries (Pricing / Sign up) as top-level items.
        // Note: getSidebarTabs must be called explicitly here because the `tabs`
        // prop accepts EITHER a config object OR an explicit array, not both.
        tabs: [
          ...getSidebarTabs(source.pageTree[lang], {
            transform(option, node) {
              if (!node.icon) return option;

              return {
                ...option,
                icon: (
                  <div className="max-md:bg-fd-primary/10 max-md:border-fd-primary/20 size-full rounded-lg max-md:border max-md:p-1.5 [&_svg]:size-full">
                    {node.icon}
                  </div>
                ),
              };
            },
          }),
          ...getPromoTabs(lang),
        ],
      }}
    >
      <BackToHome />
      {children}
      {/* AI feature temporarily disabled */}
      {/* <AISearchTrigger /> */}
    </DocsLayout>
  );
}
