import re
from pathlib import Path

batch4 = ['qr-code-with-logo', 'qr-code-for-wedding', 'qr-code-for-real-estate', 'qr-code-vs-nfc', 'qr-code-trends-2026']
for slug in batch4:
    p = Path(r'C:\Users\dell\WorkBuddy\2026-06-28-15-27-39\qr-tool\src\blog' + f'\\{slug}-content.html')
    text = p.read_text(encoding='utf-8')
    h2s = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', text)
    print(f'=== {slug} ===')
    for hid, htext in h2s:
        print(f'  h2#{hid}: {htext[:60]}')
    print()
