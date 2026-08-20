import { source } from '@/lib/source';
import { notFound } from 'next/navigation';
import { ImageResponse } from 'next/og';
import { generate as DefaultImage } from 'fumadocs-ui/og';

// Dynamic on purpose: Next 16 serves SSG route-handler responses with a
// stale text/html content-type regardless of the .meta file, which breaks
// OG image detection. Runtime generation + explicit re-wrapping of the
// response body guarantees image/png reaches the client.
export const dynamic = 'force-dynamic';

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ lang: string; slug: string[] }> }
) {
  const { lang, slug } = await params;
  const page = source.getPage(slug.slice(0, -1), lang);
  if (!page) notFound();

  const img = new ImageResponse(
    (
      <DefaultImage
        title={page.data.title}
        description={page.data.description}
        site="TokenPAPA"
      />
    ),
    {
      width: 1200,
      height: 630,
    }
  );

  const buf = await img.arrayBuffer();
  // Use a Uint8Array body — Next 16 rewrites the content-type of plain
  // ArrayBuffer responses to text/html, but leaves typed-array bodies alone.
  return new Response(new Uint8Array(buf), {
    headers: {
      'content-type': 'image/png',
      'content-length': String(buf.byteLength),
      'cache-control': 'public, max-age=86400, stale-while-revalidate=604800',
    },
  });
}
