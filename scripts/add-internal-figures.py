"""
Add comparison + scan-demo + faq-banner figures to batch4 5 posts.
For each slug, define (before_h2, figure_block) tuples in order.
"""
import re
from pathlib import Path

PROJECT = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool')
BLOG = PROJECT / 'src' / 'blog'

# (slug, [(before_h2_id, image_kind, caption), ...])
# image_kind: 'comparison' / 'scan-demo' / 'faq-banner'
FIGURES = {
    'qr-code-with-logo': [
        ('correction', 'comparison',
         'Plain black-and-white QR code vs branded QR with a center logo. Both scan, but only one feels like your brand.'),
        ('howto', 'scan-demo',
         'A 4-step workflow: enter URL, customize colors, upload logo, export. Total time: under 60 seconds.'),
        ('faq', 'faq-banner',
         'Have a logo, brand color, and 60 seconds? You have a branded QR code ready to print.'),
    ],
    'qr-code-for-wedding': [
        ('design', 'comparison',
         'Paper-heavy wedding stationery vs a QR code card. Same information, half the trees, and the bride stops chasing RSVPs.'),
        ('scanning', 'scan-demo',
         'Save-the-date → invitation → program → photo album: where each QR code lives in the wedding timeline.'),
        ('faq', 'faq-banner',
         'Pick a wedding date first, the QR codes second. They take 5 minutes once you have the URLs.'),
    ],
    'qr-code-for-real-estate': [
        ('design', 'comparison',
         'A sign with a phone number vs a sign with a QR code. One gives you a missed call at 9pm, the other gives you a lead with their email.'),
        ('analytics', 'scan-demo',
         '5 places every listing should carry a code: yard sign, flyer, open house, virtual tour, your vCard.'),
        ('faq', 'faq-banner',
         'Listing a property this week? Generate a yard sign QR code before the photographer shows up.'),
    ],
    'qr-code-vs-nfc': [
        ('head-to-head', 'comparison',
         'QR code (printed paper) vs NFC tag (tap with phone). Same outcome, very different cost and feel.'),
        ('hybrid', 'scan-demo',
         'When to pick QR (printed, free, anyone), when to pick NFC (premium, fewer taps), and when both.'),
        ('faq', 'faq-banner',
         'Start with QR. It is free, prints anywhere, and works on every phone. Add NFC when you have a reason to.'),
    ],
    'qr-code-trends-2026': [
        ('bonus-trends', 'comparison',
         '2024 static codes vs 2026 dynamic codes. Same scan, but the 2026 version tells you who scanned, when, and from which ad.'),
        ('tooling', 'scan-demo',
         'The 2026 QR stack: AI-personalized code + dynamic redirect + first-party analytics. All five layers live in your browser.'),
        ('faq', 'faq-banner',
         'Already making QR codes? Add one dynamic code this quarter. The data alone pays for the upgrade.'),
    ],
}

for slug, items in FIGURES.items():
    path = BLOG / f'{slug}-content.html'
    if not path.exists():
        print(f'  SKIP: {path.name} not found')
        continue
    text = path.read_text(encoding='utf-8')

    # Insert figures in REVERSE order so earlier inserts don't shift later markers
    for before_h2, kind, caption in reversed(items):
        img_path = f'/blog/{slug}/{slug}-{kind}.png'
        figure = (
            f'\n<figure>\n'
            f'  <img src="{img_path}" alt="{caption[:120]}" />\n'
            f'  <figcaption>{caption}</figcaption>\n'
            f'</figure>\n\n'
        )
        # Pattern: optional whitespace + <h2 id="before_h2">
        # We use lookahead to insert before the h2 without changing the h2 line
        pattern = re.compile(r'(?=\s*<h2 id="' + re.escape(before_h2) + r'")')
        new_text, n = pattern.subn(figure, text, count=1)
        if n == 0:
            print(f'  WARN: {slug} - h2#{before_h2} not found')
            continue
        text = new_text
        print(f'  OK: {slug} - added {kind} before h2#{before_h2}')

    path.write_text(text, encoding='utf-8')
print('\nDone')
