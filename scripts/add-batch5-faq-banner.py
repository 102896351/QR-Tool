"""Add faq-banner figure to batch5 2 blog posts (before <h2 id="faq">)."""
import re
from pathlib import Path

BLOG = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool\src\blog')

FIGURES = {
    'qr-code-data-capacity': (
        'A flat "max size" view of QR code capacity: 7,089 digits / 4,296 alpha / 2,953 bytes at v40-L,'
        ' with real-world safe limits of 200-500 chars. Pick the version, not the size.'
    ),
    'qr-code-for-instagram-tiktok': (
        'Bottom-right, static, on screen for 5+ seconds, pointing to a specific destination.'
        ' That is the entire playbook for QR codes in short video.'
    ),
}

for slug, caption in FIGURES.items():
    path = BLOG / f'{slug}-content.html'
    if not path.exists():
        print(f'  SKIP: {path.name} not found')
        continue
    text = path.read_text(encoding='utf-8')

    img_path = f'/blog/{slug}/{slug}-faq-banner.png'
    if img_path in text:
        print(f'  SKIP: {path.name} already has faq-banner')
        continue

    figure = (
        f'\n<figure>\n'
        f'  <img src="{img_path}" alt="{caption[:120]}" />\n'
        f'  <figcaption>{caption}</figcaption>\n'
        f'</figure>\n\n'
    )
    pattern = re.compile(r'(?=\s*<h2 id="faq")')
    new_text, n = pattern.subn(figure, text, count=1)
    if n == 0:
        print(f'  WARN: {slug} - h2#faq not found')
        continue
    path.write_text(new_text, encoding='utf-8')
    print(f'  OK: {slug} - added faq-banner before h2#faq')
