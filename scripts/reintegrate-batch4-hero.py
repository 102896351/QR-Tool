"""
Re-integrate batch4 5 content files into posts.json.
Reads each src/blog/<slug>-content.html, escapes ' to \\u2019, updates posts.json.
"""
import json
import re
from pathlib import Path

PROJECT = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool')
POSTS_JSON = PROJECT / 'src' / 'blog' / 'posts.json'

# Slugs to re-integrate
SLUGS = [
    'qr-code-with-logo',
    'qr-code-for-wedding',
    'qr-code-for-real-estate',
    'qr-code-vs-nfc',
    'qr-code-trends-2026',
]

# Load posts
posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
posts_by_slug = {p['slug']: p for p in posts}

for slug in SLUGS:
    src = PROJECT / 'src' / 'blog' / f'{slug}-content.html'
    if not src.exists():
        print(f'  SKIP: {src.name} not found')
        continue
    content = src.read_text(encoding='utf-8').strip()
    # Escape single quote to typographic apostrophe (U+2019)
    # This is how the original integrate script handled it
    content = content.replace("'", '\\u2019')
    # Update posts.json entry
    if slug in posts_by_slug:
        posts_by_slug[slug]['content'] = content
        print(f'  OK: {slug} (content length: {len(content)} chars, has figure: {"<figure>" in content})')

# Write back
POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'\nWrote {POSTS_JSON}')
