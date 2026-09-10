"""
批量博客配图重生成 —— 支持 posts.json 中任意 slug

每篇文章生 4 张图：hero / comparison / scan-demo / faq-banner
主题词由 slug/title 推断，4 种 kind 共用同一主题。

用法：
  python scripts/regen_all_blog_images.py            # 实际跑
  python scripts/regen_all_blog_images.py --dry-run  # 只打 prompt 不调 API
  python scripts/regen_all_blog_images.py --only wifi-qr-code-guide,qr-code-for-wedding
  python scripts/regen_all_blog_images.py --skip qr-code-for-healthcare  # 跳过
"""
import io
import os
import re
import json
import time
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === 复用 healthcare 版的工具函数 ===
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regen_blog_image_agnes import (
    BRAND, SITE, BRAND_RGB, BRAND_DARK_RGB, BRAND_LIGHT_RGB,
    TEXT_DARK, TEXT_MED, WHITE, BG_LIGHT, W, H, W_FAQ, H_FAQ,
    API_KEY_FILE, API_BASE,
    get_font, gradient_overlay, solid_overlay, rounded_rect,
    draw_check, make_qr_sample, draw_chip,
    _default_meta,
    make_hero as _make_hero,
    make_comparison as _make_comparison,
    make_scan_demo as _make_scan_demo,
    make_faq_banner as _make_faq_banner,
)

POSTS_JSON = "src/blog/posts.json"
SITE_BASE_DIR = "public/blog"
MARKER_DIR = "scripts/_agnes_done"   # 断点续跑标记（不入库）

# === 文件名前缀例外 ===
# 大部分文章用 "<slug>-<kind>.png"，但这三篇是早期建的，命名不一致，
# 且 posts.json 的 cover 与正文都已按旧名引用，故在此保持原名，避免改坏引用。
#   wifi-qr-code-guide        -> hero.png / comparison.png / ...
#   vcard-qr-code-guide       -> vcard-hero.png / ...
#   restaurant-qr-code-guide  -> restaurant-hero.png / ...
NAME_PREFIX = {
    "wifi-qr-code-guide": "",
    "vcard-qr-code-guide": "vcard",
    "restaurant-qr-code-guide": "restaurant",
}


def out_filename(slug: str, kind: str) -> str:
    if slug in NAME_PREFIX:
        p = NAME_PREFIX[slug]
        return f"{p}-{kind}.png" if p else f"{kind}.png"
    return f"{slug}-{kind}.png"

# === 主题词映射（slug 关键词 → 主题场景描述）===
THEME_RULES = [
    (['healthcare', 'medical', 'hospital', 'clinic'], 'modern hospital clinic with clean white interior and soft daylight'),
    (['wedding', 'bride', 'groom', 'ceremony'], 'romantic wedding ceremony with soft floral decoration'),
    (['events', 'conference', 'venue', 'ticket'], 'modern event venue or conference hall with bright lighting'),
    (['real-estate', 'apartment', 'listing', 'property'], 'modern bright apartment interior with real estate sign'),
    (['education', 'classroom', 'school', 'teacher', 'student'], 'modern classroom or lecture hall with educational atmosphere'),
    (['restaurant', 'menu', 'dining', 'cafe', 'food'], 'modern restaurant interior with dining table and menu'),
    (['email', 'gmail', 'inbox', 'mail'], 'modern email workspace with laptop and clean desk'),
    (['form', 'survey'], 'online form interface on modern computer screen'),
    (['sms', 'text-message'], 'smartphone with text messaging interface'),
    (['pdf', 'document'], 'modern document workspace with papers'),
    (['instagram', 'tiktok', 'social'], 'social media scene with smartphone and creative content'),
    (['nonprofit', 'charity', 'fundraising'], 'warm community charity event with volunteers'),
    (['safe', 'security', 'phishing', 'secure'], 'abstract cybersecurity digital lock interface'),
    (['best', 'free', 'review', 'generator', 'comparison'], 'modern tech workspace with multiple devices comparison'),
    (['dynamic', 'static'], 'modern tech comparison workspace'),
    (['how-qr-code', 'anatomy', 'history', 'evolution'], 'abstract technology code matrix visualization'),
    (['scan', 'screenshot'], 'smartphone scanning QR code close-up'),
    (['make', 'create', 'link', 'url'], 'modern web workspace with URL bar on laptop'),
    (['data-capacity', 'statistics', 'trends'], 'modern data visualization dashboard with charts'),
    (['design', 'logo', 'branding', 'size', 'style'], 'modern graphic design studio workspace'),
    (['error', 'correction', 'fix', 'broken'], 'technology debugging abstract scene'),
    (['vs-barcode', 'vs-nfc'], 'modern technology comparison interface'),
    (['vcard', 'business-card'], 'modern business card with contact information'),
    (['wifi'], 'modern home or cafe with WiFi router and devices connecting'),
]


def theme_for_slug(slug: str, title: str = "") -> str:
    """根据 slug 推断主题场景描述。"""
    s = (slug + " " + title).lower()
    for keywords, theme in THEME_RULES:
        for kw in keywords:
            if kw in s:
                # 清理掉模板里会重复的修饰词
                return theme
    return 'modern clean tech workspace with soft natural lighting'


def build_prompt(kind: str, theme: str) -> str:
    """构造 prompt，自动去除 'modern modern' 这类重复修饰词。"""
    raw = PROMPT_TEMPLATES[kind].format(theme=theme)
    # 去除重复的修饰词（模板里 + 主题词里都有）
    for word in ("modern", "clean", "bright"):
        while f"{word} {word}" in raw.lower():
            raw = re.sub(rf"\b{word} {word}\b", word, raw, flags=re.IGNORECASE)
    return raw


# === 4 种 kind 的 prompt 模板 ===
PROMPT_TEMPLATES = {
    "hero": (
        "A bright, clean {theme} scene, soft natural daylight, minimalist modern interior, "
        "professional photography, ultra clean composition, subject on the right side "
        "leaving generous space on the left for text overlay, no people, no text, no logo"
    ),
    "comparison": (
        "A clean modern {theme} setting with a tablet computer on a desk, "
        "soft daylight from windows, minimalist interior, no text, no people, "
        "professional photography, shallow depth of field"
    ),
    "scan-demo": (
        "A close-up photo of a hand holding a smartphone scanning a QR code, "
        "{theme} setting in the background, soft focus, bright clean lighting, "
        "realistic photojournalism style, no text, no people faces visible, "
        "shallow depth of field focusing on the phone screen"
    ),
    "faq-banner": (
        "A serene {theme} interior with soft daylight, modern clean atmosphere, "
        "no people, no text, professional interior photography, calm and trustworthy mood"
    ),
}

SIZE_MAP = {
    "hero": "1536x1024",
    "comparison": "1536x1024",
    "scan-demo": "1536x1024",
    "faq-banner": "1536x512",
}

# === Agnes 调用 ===
def agnes_generate(prompt, size, retries=3):
    with open(API_KEY_FILE) as f:
        key = f.read().strip()
    for attempt in range(retries):
        r = subprocess.run(
            ["curl", "-s", "-m", "120", "-X", "POST", f"{API_BASE}/images/generations",
             "-H", f"Authorization: Bearer {key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps({
                 "model": "agnes-image-2.1-flash",
                 "prompt": prompt,
                 "size": size,
             })],
            capture_output=True, text=True, timeout=130,
        )
        try:
            d = json.loads(r.stdout)
        except json.JSONDecodeError:
            time.sleep(8)
            continue
        if "data" in d and d["data"]:
            return d["data"][0]["url"]
        if "error" in d:
            print(f"    [ERROR] {d['error'].get('message', '')[:150]}")
        time.sleep(8)
    raise RuntimeError(f"Agnes 生图失败")


def download(url, out_path):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    return Image.open(out_path).convert("RGB")


# === 单篇处理 ===
def process_post(post, kinds, tmp_dir, dry_run=False, force=False):
    slug = post["slug"]
    title = post.get("title", "")
    theme = theme_for_slug(slug, title)
    out_dir = f"{SITE_BASE_DIR}/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tmp_dir, exist_ok=True)

    print(f"\n  ▸ {slug}  ({title[:40]})  theme: {theme[:60]}")
    for kind in kinds:
        prompt = build_prompt(kind, theme)
        size = SIZE_MAP[kind]
        out_path = f"{out_dir}/{out_filename(slug, kind)}"

        if dry_run:
            print(f"    [{kind:12}] size={size}  -> {out_path}")
            print(f"      prompt: {prompt[:110]}...")
            continue

        if not force and os.path.exists(f"{MARKER_DIR}/{slug}--{kind}.ok"):
            print(f"    [{kind}] 已由 Agnes 生成过，跳过（--force 可覆盖）")
            continue

        try:
            print(f"    [{kind}] 生图...")
            url = agnes_generate(prompt, size)
            tmp_path = f"{tmp_dir}/{slug}-{kind}.jpg"
            base_img = download(url, tmp_path)

            # 调合成函数（必须传 meta：每个合成函数都靠 meta 里的 slug/title/sub
            # 决定写什么文字 + 生成对应二维码 URL；不传就会用 healthcare 默认，
            # 整批图都会变成「QR Codes in Healthcare + 药签」）
            # kind 名要转成 _default_meta 里的 key（hero/scan-demo → scan_demo/faq）
            meta_kind = {"scan-demo": "scan_demo", "faq-banner": "faq"}.get(kind, kind)
            meta = _default_meta(slug, title, meta_kind)
            if kind == "hero":
                _make_hero(base_img, meta, out_path)
            elif kind == "comparison":
                _make_comparison(base_img, meta, out_path)
            elif kind == "scan-demo":
                _make_scan_demo(base_img, meta, out_path)
            elif kind == "faq-banner":
                _make_faq_banner(base_img, meta, out_path)

            sz_kb = os.path.getsize(out_path) // 1024
            # 打标记：区分 Agnes 产物与早期 Picsum 图，便于中断后断点续跑。
            # 标记放在 scripts/ 下而非 public/，避免被打包进站点。
            os.makedirs(MARKER_DIR, exist_ok=True)
            open(f"{MARKER_DIR}/{slug}--{kind}.ok", "w").write("agnes-image-2.1-flash\n")
            print(f"    [{kind}] → {sz_kb} KB ✓")
            time.sleep(2.5)   # 限流保护：每张间隔 2.5s ≈ 24 RPM，Agnes 限额通常 60 RPM
        except Exception as e:
            FAILED.append((slug, kind, str(e)))
            print(f"    [{kind}] FAILED: {e}")
            time.sleep(5)


FAILED = []


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只打 prompt 不调 API")
    ap.add_argument("--only", default="", help="只跑指定 slug（逗号分隔）")
    ap.add_argument("--skip", default="", help="跳过指定 slug（逗号分隔）")
    ap.add_argument("--kinds", default="hero,comparison,scan-demo,faq-banner",
                    help="跑哪些 kind")
    ap.add_argument("--force", action="store_true", help="已存在的图也重新生成")
    args = ap.parse_args()

    kinds = args.kinds.split(",")
    only_set = set(s.strip() for s in args.only.split(",") if s.strip())
    skip_set = set(s.strip() for s in args.skip.split(",") if s.strip())

    posts = json.load(open(POSTS_JSON, encoding="utf-8"))
    print(f"[批量] 共 {len(posts)} 篇")
    if args.dry_run:
        print("[DRY-RUN] 只打 prompt，不调 API")
    print(f"[kinds] {kinds}")
    if only_set: print(f"[only] {sorted(only_set)}")
    if skip_set: print(f"[skip] {sorted(skip_set)}")
    if args.force: print("[force] 已存在的图也会重生成")

    tmp_dir = "scripts/_tmp_agnes"
    for post in posts:
        slug = post["slug"]
        if only_set and slug not in only_set:
            continue
        if skip_set and slug in skip_set:
            print(f"\n  ⊘ {slug} (skipped)")
            continue
        process_post(post, kinds, tmp_dir, dry_run=args.dry_run, force=args.force)

    if FAILED:
        print(f"\n[!] {len(FAILED)} 张失败：")
        for slug, kind, err in FAILED:
            print(f"    {slug} / {kind}: {err[:120]}")
        print("    重跑同一条命令即可续跑（已存在的会自动跳过）")
    print(f"\n[✓] 完成")


if __name__ == "__main__":
    main()