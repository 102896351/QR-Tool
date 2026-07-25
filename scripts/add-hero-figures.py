"""
Add hero figure to batch4 5 blog posts.
Insert <figure> block right before the first <h2> in each content file.
"""
import re
from pathlib import Path

CONTENT_DIR = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool\src\blog')

# Hero figure blocks for each batch4 post
HERO_FIGURES = {
    'qr-code-with-logo': {
        'img_alt': 'QR code with logo: how to add a brand mark without breaking scans',
        'caption': 'A branded QR code with center logo. Error correction level H keeps it scannable.'
    },
    'qr-code-for-wedding': {
        'img_alt': 'QR code for wedding: save the date card with RSVP code',
        'caption': 'A save-the-date card carrying a scan-to-RSVP code. Modern weddings lean heavily on this.'
    },
    'qr-code-for-real-estate': {
        'img_alt': 'QR code for real estate: yard sign with lead-capture code',
        'caption': 'A yard sign combining a phone number fallback and a QR code that captures leads 24/7.'
    },
    'qr-code-vs-nfc': {
        'img_alt': 'QR code vs NFC: side-by-side comparison of a printed code and a tap tag',
        'caption': 'QR code on the left, NFC tag on the right. Both work; the use case decides.'
    },
    'qr-code-trends-2026': {
        'img_alt': 'QR code trends 2026: dynamic personalized code with analytics dashboard',
        'caption': 'A dynamic, personalized QR code with backend analytics — the shape of 2026.'
    },
}

for slug, info in HERO_FIGURES.items():
    path = CONTENT_DIR / f'{slug}-content.html'
    if not path.exists():
        print(f'  SKIP: {path.name} not found')
        continue

    text = path.read_text(encoding='utf-8')

    # Check if hero figure already exists
    if f'/{slug}/{slug}-hero.png' in text:
        print(f'  SKIP: {path.name} already has hero figure')
        continue

    # Build the figure block
    figure_block = (
        f'\n<figure>\n'
        f'  <img src="/blog/{slug}/{slug}-hero.png" alt="{info["img_alt"]}" />\n'
        f'  <figcaption>{info["caption"]}</figcaption>\n'
        f'</figure>\n\n'
    )

    # Insert before the first <h2>
    new_text, n = re.subn(r'(?=\s*<h2)', figure_block, text, count=1)
    if n == 0:
        print(f'  SKIP: {path.name} no <h2> found')
        continue

    path.write_text(new_text, encoding='utf-8')
    print(f'  OK: {path.name} (hero figure added before first h2)')
