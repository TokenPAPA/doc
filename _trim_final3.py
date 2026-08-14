#!/usr/bin/env python3
"""Hard-trim descriptions to ~150 chars at word boundaries."""
import re, glob

def hard_trim(text):
    text = text.strip()
    if len(text) <= 155:
        return text
    # Cut at last space before 152
    idx = text.rfind(' ', 130, 152)
    if idx > 130:
        result = text[:idx].rstrip('.,;: ')
        return result + '.'
    # Fallback
    return text[:150].rstrip('.,;: ') + '.'

base = 'content/docs/en/blog'
total = 0

for path in sorted(glob.glob(f'{base}/*.mdx')):
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
        continue
    
    old = m.group(1).strip()
    if len(old) <= 155:
        continue
    
    new = hard_trim(old)
    if len(new) < 130:
        print(f"  WARNING {name}: still only {len(new)} chars")
    
    header = header.replace(m.group(0), f'description: "{new}"')
    
    with open(path, 'w') as f:
        f.write(f'---\n{header}---\n{body}')
    
    total += 1
    print(f"  {name}: {len(old)} -> {len(new)} chars")

print(f'\nDone! {total} trimmed.')
