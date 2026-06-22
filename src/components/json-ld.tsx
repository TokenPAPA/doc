'use client';

/**
 * JsonLd — safely injects JSON-LD structured data into the page <head>.
 * Use in MDX as: <JsonLd json={JSON.stringify({ "@context": "https://schema.org", ... })} />
 * The stringified data is embedded in the page so crawlers can find it.
 */
export function JsonLd({ json: jsonString }: { json: string }) {
  const jsonLd = jsonString;

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: jsonLd }}
    />
  );
}
