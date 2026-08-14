#!/usr/bin/env python3
"""Trim blog descriptions that exceed 160 chars. Keep only what's over."""

import re, glob

def smart_trim(text):
    """Trim description to at most 155 chars, cutting cleanly."""
    text = text.strip()
    if len(text) <= 155:
        return text
    
    # Cut at 155
    cut = text[:155]
    
    # Try to end at a sentence boundary (working backwards from 155)
    last_period = cut.rfind('. ')
    if last_period > 80:  # Only if we'd keep enough text
        return text[:last_period + 1]
    
    # Try last word boundary
    last_space = cut.rfind(' ')
    if last_space > 80:
        result = text[:last_space]
        # Remove trailing punctuation
        result = result.rstrip('.,;:,- ')
        return result + '.'
    
    # Hard cut
    return text[:152].rstrip('.,;: ') + '...'

base = '/home/newApi/tokenpapa-doc/content/docs'
total_trimmed = 0

for lang in ['en', 'zh', 'ja']:
    for path in sorted(glob.glob(f'{base}/{lang}/blog/*.mdx')):
        name = path.split('/')[-1].replace('.mdx', '')
        if name == 'index':
            continue
        
        with open(path) as f:
            content = f.read()
        
        # Parse frontmatter to find description
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            continue
        
        header = parts[1]
        body = parts[2]
        
        # Find description line
        m = re.search(r'^description:\s*"(.+?)"', header, re.MULTILINE)
        if not m:
            m = re.search(r"^description:\s*'(.+?)'", header, re.MULTILINE)
        if not m:
            m = re.search(r'^description:\s*(.+?)$', header, re.MULTILINE)
        
        if not m:
            print(f"  {lang}/{name}: no description found")
            continue
        
        old_desc = m.group(1).strip()
        old_len = len(old_desc)
        
        if old_len <= 155:
            continue
        
        new_desc = smart_trim(old_desc)
        new_len = len(new_desc)
        
        # Replace in header
        old_line = m.group(0)
        new_line = f'description: "{new_desc}"'
        header = header.replace(old_line, new_line)
        
        # Rebuild
        new_content = f'---\n{header}---\n{body}'
        with open(path, 'w') as f:
            f.write(new_content)
        
        total_trimmed += 1
        print(f"  {lang}/{name}: {old_len} -> {new_len} chars")

print(f'\nDone! {total_trimmed} descriptions trimmed.')
