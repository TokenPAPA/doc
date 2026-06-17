'use client';

import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { House } from 'lucide-react';
import { cn } from '@/lib/cn';

/**
 * "Back to Home" pinned to the right of the Fumadocs top tab bar.
 *
 * The docs layout renders the tab bar (`LayoutTabs`) as a flex row with no slot
 * for extra content, so we portal the link into that bar as its last child and
 * push it right with `ms-auto`. It is styled as a plain text + icon link that
 * matches the tabs (muted text, accent on hover, `pb-1.5` baseline) rather than
 * a boxed button, so it reads as part of the bar.
 * The bar is `max-md:hidden`, so the link is hidden on mobile, where the top
 * navbar logo already links home.
 */
export function BackToHome() {
  const [bar, setBar] = useState<HTMLElement | null>(null);

  useEffect(() => {
    setBar(
      document.querySelector<HTMLElement>(
        '#nd-docs-layout > div.sticky.border-b',
      ),
    );
  }, []);

  if (!bar) return null;

  return createPortal(
    <a
      href="https://tokenpapa.ai"
      target="_blank"
      rel="noreferrer noopener"
      className={cn(
        'ms-auto inline-flex shrink-0 items-center gap-1.5 pb-1.5 text-sm font-medium',
        'text-fd-muted-foreground transition-colors hover:text-fd-accent-foreground',
      )}
    >
      <House className="size-4" />
      Back to Home
    </a>,
    bar,
  );
}
