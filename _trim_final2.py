#!/usr/bin/env python3
"""Smart-trim blog descriptions to 140-155 chars, preserving sentences."""
import re, glob

def smart_trim(text):
    text = text.strip()
    if len(text) <= 155:
        return text
    
    # Target: 140-155 chars
    # Strategy: find the last sentence-ending period in [130, 155]
    target = text[:155]
    
    # Look for sentence endings in range [130:155]
    candidates = []
    for sep in ['. ', '? ', '! ']:
        idx = -1
        while True:
            idx = target.find(sep, idx + 1)
            if idx == -1:
                break
            if 130 <= idx + len(sep) <= 155:
                candidates.append(idx + len(sep))
    
    if candidates:
        pick = max(candidates)  # Closest to 155
        result = text[:pick].rstrip(' ,;:')
        if 130 <= len(result) <= 155:
            return result + '.'
    
    # No sentence boundary found: cut at last word boundary near 150
    cut_at = 150
    idx = text.rfind(' ', 100, cut_at)
    if idx > 100:
        result = text[:idx].rstrip('.,;: ')
        if len(result) >= 120:
            return result + '.'
    
    # Fallback: hard cut
    return text[:152].rstrip('.,;: ') + '.'

base = '/home/newApi/tokenpapa-doc/content/docs'
total = 0

for lang in ['en', 'zh', 'ja']:
    for path in sorted(glob.glob(f'{base}/{lang}/blog/*.mdx')):
        name = path.split('/')[-1].replace('.mdx', '')
        if name == 'index':
            continue
        
        with open(path) as f:
            content = f.read()
        
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            continue
        
        header, body = parts[1], parts[2]
        
        m = re.search(r'^description:\s*"(.+?)"', header, re.MULTILINE)
        if not m:
            m = re.search(r"^description:\s*'(.+?)'", header, re.MULTILINE)
        if not m:
            m = re.search(r'^description:\s*(.+?)$', header, re.MULTILINE)
        if not m:
            continue
        
        old = m.group(1).strip()
        if len(old) <= 155:
            continue
        
        new = smart_trim(old)
        if len(new) < 130:
            # Too short - retry with hard cut at 150
            idx = old.rfind(' ', 100, 150)
            if idx > 100:
                new = old[:idx].rstrip('.,;: ') + '.'
            else:
                new = old[:150].rstrip('.,;: ') + '.'
        
        old_line = m.group(0)
        new_line = f'description: "{new}"'
        header = header.replace(old_line, new_line)
        
        with open(path, 'w') as f:
            f.write(f'---\n{header}---\n{body}')
        
        total += 1
        print(f"  {lang}/{name}: {len(old)} -> {len(new)} chars")
        
        # Flag if still problematic
        if len(new) < 130:
            print(f"    WARNING: only {len(new)} chars!")

print(f'\nDone! {total} descriptions fixed.')
