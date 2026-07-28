"""Integrate batch5 2 blog posts (data-capacity + instagram-tiktok) into posts.json."""
import json
from pathlib import Path

PROJECT = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool')
POSTS_JSON = PROJECT / 'src' / 'blog' / 'posts.json'

# New posts to append
NEW_POSTS = [
    {
        'slug': 'qr-code-data-capacity',
        'title': 'QR Code Data Capacity: How Much Can a QR Code Actually Store?',
        'description': 'Max 7,089 digits, 4,296 alphanumeric characters, 2,953 bytes, or 1,468 Chinese characters. Here is the real QR code storage limit per version, per error correction, per character set.',
        'category': 'Data',
        'date': '2026-07-28',
        'readTime': 9,
        'author': 'QR Tool Studio',
        'cover': '/blog/qr-code-data-capacity/qr-code-data-capacity-hero.png',
        'tags': [
            'qr-code',
            'capacity',
            'storage',
            'data',
            'version',
            'spec',
            'iso-18004',
        ],
    },
    {
        'slug': 'qr-code-for-instagram-tiktok',
        'title': 'QR Code for Instagram and TikTok: How to Make Codes That Actually Get Scanned',
        'description': 'Most QR codes in short video get ignored. Here are the 4 placement rules, the size math for 9:16, the contrast and color guidelines, and the link strategy that makes TikTok QR codes work.',
        'category': 'How-To',
        'date': '2026-07-28',
        'readTime': 11,
        'author': 'QR Tool Studio',
        'cover': '/blog/qr-code-for-instagram-tiktok/qr-code-for-instagram-tiktok-hero.png',
        'tags': [
            'qr-code',
            'instagram',
            'tiktok',
            'short-video',
            'reels',
            'placement',
            'design',
        ],
    },
]

posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
existing_slugs = {p['slug'] for p in posts}
print(f'Loaded {len(posts)} existing posts')

added = 0
for spec in NEW_POSTS:
    slug = spec['slug']
    if slug in existing_slugs:
        print(f'  SKIP: {slug} already in posts.json')
        continue
    content_path = PROJECT / 'src' / 'blog' / f'{slug}-content.html'
    if not content_path.exists():
        print(f'  SKIP: {slug} content file missing')
        continue
    content = content_path.read_text(encoding='utf-8').strip()
    # Escape single quote to typographic apostrophe (U+2019) — match batch4 integrate
    content = content.replace("'", '\\u2019')
    spec['content'] = content
    posts.append(spec)
    print(f'  OK: {slug} (content {len(content)} chars, has 4 figures: '
          f'hero={f"/blog/{slug}/{slug}-hero.png" in content}, '
          f'cmp={f"/blog/{slug}/{slug}-comparison.png" in content}, '
          f'scan={f"/blog/{slug}/{slug}-scan-demo.png" in content}, '
          f'faq={f"/blog/{slug}/{slug}-faq-banner.png" in content})')
    added += 1

POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'\nAdded {added} posts. Total now: {len(posts)}')
