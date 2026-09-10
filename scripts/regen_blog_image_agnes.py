"""
博客配图重生成脚本 —— Agnes AI 主题图版（demo：qr-code-for-healthcare）

流程：
  1) 调用 agnes-image-2.1-flash 生 4 张医疗主题底图（无文字，便于叠加）
  2) 下载图
  3) Pillow 叠加：品牌色遮罩 + 文字 + 二维码示例 + 修正 example.com → 真实域名

依赖：pillow + qrcode（已装）— 用 curl 调 Agnes，绕开 openai 包的安装
"""
import io
import os
import json
import time
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =============== 主题配置 ===============
BRAND = "QR Tool Studio"
SITE = "toolbox168.xyz"   # 修正 example.com bug
SLUG = "qr-code-for-healthcare"
OUTPUT_DIR = f"public/blog/{SLUG}"

BRAND_RGB = (99, 102, 241)
BRAND_DARK_RGB = (79, 70, 229)
BRAND_LIGHT_RGB = (199, 210, 254)
TEXT_DARK = (30, 41, 59)
TEXT_MED = (71, 85, 105)
WHITE = (255, 255, 255)
BG_LIGHT = (248, 250, 252)

W, H = 1200, 630
W_FAQ, H_FAQ = 1200, 400

API_KEY_FILE = "C:/Users/dell/.workbuddy/agnes_key.txt"
API_BASE = "https://apihub.agnes-ai.com/v1"

# =============== 4 张主题图 prompt ===============
# 注意：明确要求 "no text" 让 AI 不要生成难看的英文/中文乱字
# 构图上要求主体偏左或下，给右侧/上方留白以便叠文字
PROMPTS = {
    "hero": {
        "size": "1536x1024",   # 16:9 多一点 → resize 到 1200x630
        "prompt": (
            "A bright, modern hospital reception area with floor-to-ceiling windows, "
            "soft natural sunlight streaming in, minimalist white and glass interior, "
            "medical corridor leading into the background, no people, no text, no logo, "
            "professional architectural photography, ultra clean composition, "
            "subject on the right side leaving space on the left for text overlay"
        ),
    },
    "comparison": {
        "size": "1536x1024",
        "prompt": (
            "A clean modern clinic registration desk with a tablet computer on the counter, "
            "medical forms and folders nearby, soft daylight from windows, "
            "minimalist white interior with teal accents, no text, no people, "
            "professional healthcare photography, shallow depth of field"
        ),
    },
    "scan-demo": {
        "size": "1536x1024",
        "prompt": (
            "A close-up photo of a hand holding a smartphone scanning a QR code on a white "
            "prescription medicine bottle, soft focus medical background, "
            "bright clean lighting, realistic photojournalism style, no text, "
            "shallow depth of field focusing on the phone screen"
        ),
    },
    "faq-banner": {
        "size": "1536x512",    # 3:1 → resize 到 1200x400
        "prompt": (
            "A serene hospital consultation room with soft daylight, modern medical "
            "equipment in the background, comfortable chair, no people, no text, "
            "professional interior photography, calm and trustworthy mood"
        ),
    },
}


# =============== Agnes 调用 ===============
def agnes_generate(kind, retries=3):
    spec = PROMPTS[kind]
    prompt = spec["prompt"]
    size = spec["size"]
    with open(API_KEY_FILE) as f:
        key = f.read().strip()

    for attempt in range(retries):
        print(f"  [Agnes] {kind}: prompt 生图（attempt {attempt+1}/{retries}）...")
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
            print(f"  [parse fail] {r.stdout[:200]}")
            time.sleep(5)
            continue
        if "data" in d and d["data"]:
            url = d["data"][0]["url"]
            print(f"  [OK] → {url[:70]}...")
            return url
        if "error" in d:
            err = d["error"]
            print(f"  [ERROR] {err.get('message', err)[:200]}")
            # 限流等可重试错误
            time.sleep(8)
            continue
        print(f"  [unknown resp] {r.stdout[:200]}")
        time.sleep(5)
    raise RuntimeError(f"Agnes 生图失败：{kind}")


def download(url, out_path, retries=3):
    for i in range(retries):
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(r.content)
            return Image.open(out_path).convert("RGB")
        time.sleep(3)
    raise RuntimeError(f"下载失败：{url}")


# =============== Pillow 合成工具 ===============
def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def gradient_overlay(img, color, direction="left", alpha_start=220, alpha_end=0):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for x in range(w):
        t = x / w if direction == "left" else (1 - x / w) if direction == "right" else 0
        a = int(alpha_start + (alpha_end - alpha_start) * t)
        for y in range(h):
            overlay.putpixel((x, y), (color[0], color[1], color[2], a))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def solid_overlay(img, color, alpha=200):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_check(draw, xy, size, color):
    """用 polygon 画勾选符号（避免 Unicode 字符字体问题）。"""
    x, y = xy
    # 勾的三个点：左下 → 中下 → 右上
    pts = [
        (x + size * 0.15, y + size * 0.55),
        (x + size * 0.40, y + size * 0.78),
        (x + size * 0.85, y + size * 0.30),
    ]
    draw.line([pts[0], pts[1], pts[2]], fill=color, width=max(3, int(size * 0.13)))


def make_qr_sample(text, size=180):
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=0)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="#1e293b", back_color="white").convert("RGB")
    return img.resize((size, size), Image.LANCZOS)


def draw_chip(draw, xy, text, font, bg=BRAND_LIGHT_RGB, fg=BRAND_DARK_RGB):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 18, 10
    w = tw + pad_x * 2
    h = th + pad_y * 2
    rounded_rect(draw, (x, y, x + w, y + h), radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 3), text, font=font, fill=fg)
    return x + w


# =============== 4 张图合成 ===============
def make_hero(base):
    img = gradient_overlay(base.resize((W, H)), BRAND_RGB, direction="left",
                           alpha_start=235, alpha_end=50)
    draw = ImageDraw.Draw(img)

    f_label = get_font(18, bold=True)
    draw.text((60, 70), "HEALTHCARE  ·  GUIDE", font=f_label, fill=BRAND_LIGHT_RGB)

    f_title = get_font(58, bold=True)
    draw.text((60, 110), "QR Codes in", font=f_title, fill=WHITE)
    draw.text((60, 175), "Healthcare", font=f_title, fill=WHITE)

    f_sub = get_font(22)
    draw.text((60, 260), "7 ways clinics & hospitals", font=f_sub, fill=(224, 231, 255))
    draw.text((60, 290), "use them in 2025", font=f_sub, fill=(224, 231, 255))

    f_chip = get_font(16, bold=True)
    chip_x, chip_y = 60, 360
    for tag in ["Patient Intake", "Wayfinding", "Lab Results", "Medication"]:
        chip_x = draw_chip(draw, (chip_x, chip_y), tag, f_chip) + 10

    f_brand = get_font(15)
    draw.text((60, H - 45), f"{BRAND}  ·  {SITE}", font=f_brand, fill=(199, 210, 254))

    # 真实二维码示例
    qr_img = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=170)
    qr_bg = Image.new("RGBA", (qr_img.size[0] + 24, qr_img.size[1] + 24), (255, 255, 255, 255))
    qr_bg.paste(qr_img, (12, 12))
    shadow = Image.new("RGBA", qr_bg.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((4, 6, qr_bg.size[0] - 1, qr_bg.size[1] - 1),
                         radius=12, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img.paste(shadow, (W - qr_bg.size[0] - 60 + 4, H - qr_bg.size[1] - 50 + 6), shadow)
    img.paste(qr_bg, (W - qr_bg.size[0] - 60, H - qr_bg.size[1] - 50))

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-hero.png"), "PNG", optimize=True)


def make_comparison(base):
    img = solid_overlay(base.resize((W, H)), BG_LIGHT, alpha=210)
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, W, 6), fill=BRAND_RGB)

    f_title = get_font(36, bold=True)
    f_sub = get_font(18)
    draw.text((60, 50), "Paper Intake vs QR Intake", font=f_title, fill=TEXT_DARK)
    draw.text((60, 100), "Same clinic. Same patient. Different result.",
              font=f_sub, fill=TEXT_MED)

    # 左边：Before
    card1 = (60, 170, 580, 540)
    rounded_rect(draw, card1, radius=20, fill=WHITE, outline=(226, 232, 240), width=2)
    draw.text((90, 195), "BEFORE", font=get_font(20, bold=True), fill=(220, 38, 38))
    draw.text((90, 235), "Paper Clipboard", font=get_font(24, bold=True), fill=TEXT_DARK)
    px, py = 90, 290
    for i in range(5):
        rounded_rect(draw, (px + i * 4, py + i * 4,
                            px + 380 + i * 4, py + 200 + i * 4),
                     radius=4, fill=(254, 240, 138), outline=(202, 138, 4), width=2)
    for line_i in range(4):
        y = py + 40 + line_i * 28
        draw.line([(px + 20, y), (px + 360, y)], fill=(202, 138, 4), width=3)
    draw.text((px, py + 220), "10 min", font=get_font(36, bold=True), fill=(220, 38, 38))
    draw.text((px + 130, py + 232), "per patient", font=get_font(16), fill=TEXT_MED)

    # 右边：After
    card2 = (620, 170, W - 60, 540)
    rounded_rect(draw, card2, radius=20, fill=(220, 252, 231), outline=(34, 197, 94), width=2)
    draw.text((650, 195), "AFTER", font=get_font(20, bold=True), fill=(22, 163, 74))
    draw.text((650, 235), "QR Code Check-in", font=get_font(24, bold=True), fill=TEXT_DARK)

    ph_x, ph_y = 700, 290
    ph_w, ph_h = 200, 240
    rounded_rect(draw, (ph_x, ph_y, ph_x + ph_w, ph_y + ph_h), radius=24, fill=(30, 41, 59))
    rounded_rect(draw, (ph_x + 10, ph_y + 20, ph_x + ph_w - 10, ph_y + ph_h - 30),
                 radius=8, fill=(248, 250, 252))
    inner_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=150)
    img.paste(inner_qr, (ph_x + 25, ph_y + 35))
    # 绿色 check 标识（用 polygon 画）
    check_x, check_y = ph_x + ph_w - 50, ph_y + ph_h - 70
    rounded_rect(draw, (check_x, check_y, check_x + 36, check_y + 36), radius=18, fill=(22, 163, 74))
    draw_check(draw, (check_x + 3, check_y + 3), 30, WHITE)
    draw.text((650, ph_y + ph_h + 10), "90 sec", font=get_font(36, bold=True), fill=(22, 163, 74))
    draw.text((780, ph_y + ph_h + 22), "per patient", font=get_font(16), fill=TEXT_MED)

    f_kicker = get_font(15, bold=True)
    draw.text((W // 2, H - 50),
              "Saves 8 min per patient  ·  2.5 kg less paper per day  ·  88% patient open rate",
              font=f_kicker, fill=BRAND_DARK_RGB, anchor="mm")

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-comparison.png"), "PNG", optimize=True)


def make_scan_demo(base):
    img = solid_overlay(base.resize((W, H)), (240, 249, 255), alpha=215)
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_sub = get_font(17)
    draw.text((60, 50), "Patient scans QR on prescription label", font=f_title, fill=TEXT_DARK)
    draw.text((60, 95), "Verified medication, dose, and refill status — no app, no signup.",
              font=f_sub, fill=TEXT_MED)

    # 左：药签
    rx_x, rx_y = 100, 170
    rx_w, rx_h = 280, 380
    rounded_rect(draw, (rx_x, rx_y, rx_x + rx_w, rx_y + rx_h), radius=16,
                 fill=WHITE, outline=(226, 232, 240), width=2)
    rounded_rect(draw, (rx_x + 20, rx_y + 20, rx_x + rx_w - 20, rx_y + 80),
                 radius=8, fill=(59, 130, 246))
    rounded_rect(draw, (rx_x + 20, rx_y + 100, rx_x + rx_w - 20, rx_y + 220),
                 radius=8, fill=(254, 240, 138))
    draw.text((rx_x + 35, rx_y + 115), "Amoxicillin 500mg", font=get_font(16, bold=True), fill=TEXT_DARK)
    draw.text((rx_x + 35, rx_y + 145), "Take 1 cap, 3x daily", font=get_font(13), fill=TEXT_DARK)
    draw.text((rx_x + 35, rx_y + 168), "Rx #847291", font=get_font(12), fill=TEXT_MED)
    rx_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=120)
    img.paste(rx_qr, (rx_x + 80, rx_y + 230))

    # 中：箭头
    arrow_y = rx_y + 180
    draw.line([(rx_x + rx_w + 30, arrow_y), (rx_x + rx_w + 130, arrow_y)],
              fill=BRAND_RGB, width=6)
    draw.polygon([(rx_x + rx_w + 130, arrow_y - 12),
                  (rx_x + rx_w + 160, arrow_y),
                  (rx_x + rx_w + 130, arrow_y + 12)], fill=BRAND_RGB)

    # 右：手机
    ph_x, ph_y = 580, 160
    ph_w, ph_h = 220, 400
    rounded_rect(draw, (ph_x, ph_y, ph_x + ph_w, ph_y + ph_h), radius=28, fill=(15, 23, 42))
    rounded_rect(draw, (ph_x + 12, ph_y + 30, ph_x + ph_w - 12, ph_y + ph_h - 40),
                 radius=10, fill=(241, 245, 249))
    fx, fy = ph_x + 50, ph_y + 80
    rounded_rect(draw, (fx, fy, fx + 120, fy + 120), radius=6, outline=(34, 197, 94), width=4)
    phone_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=90)
    img.paste(phone_qr, (fx + 15, fy + 15))
    vb_x, vb_y = ph_x + 75, ph_y + 230
    rounded_rect(draw, (vb_x, vb_y, vb_x + 70, vb_y + 70), radius=35, fill=(22, 163, 74))
    draw_check(draw, (vb_x + 15, vb_y + 12), 40, WHITE)
    draw.text((ph_x + ph_w // 2, vb_y + 80), "Verified", font=get_font(16, bold=True),
              fill=(22, 163, 74), anchor="mm")

    # 右下角：成功结果盒
    right_x, right_y = ph_x + ph_w + 50, arrow_y - 60
    rounded_rect(draw, (right_x, right_y, right_x + 100, right_y + 120),
                 radius=12, outline=BRAND_RGB, width=3, fill=WHITE)
    # 盒内简笔画表示记录条目
    draw.line([(right_x + 12, right_y + 28), (right_x + 88, right_y + 28)],
              fill=TEXT_DARK, width=3)
    draw.line([(right_x + 12, right_y + 48), (right_x + 78, right_y + 48)],
              fill=TEXT_DARK, width=3)
    draw.line([(right_x + 12, right_y + 68), (right_x + 70, right_y + 68)],
              fill=TEXT_DARK, width=3)
    # ✓
    rounded_rect(draw, (right_x + 25, right_y + 80, right_x + 75, right_y + 110),
                 radius=8, fill=(22, 163, 74))
    draw_check(draw, (right_x + 35, right_y + 86), 28, WHITE)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-scan-demo.png"), "PNG", optimize=True)


def make_faq_banner(base):
    img = gradient_overlay(base.resize((W_FAQ, H_FAQ)), BRAND_RGB, direction="left",
                           alpha_start=210, alpha_end=120)
    draw = ImageDraw.Draw(img)

    f_title = get_font(30, bold=True)
    f_sub = get_font(16)
    draw.text((60, 40), "6 Questions About QR Codes in Healthcare", font=f_title, fill=WHITE)
    draw.text((60, 80), "The answers patients and clinic staff ask most", font=f_sub, fill=BRAND_LIGHT_RGB)

    qs = ["HIPAA compliant?", "What size?", "Static or dynamic?",
          "Infection risk?", "No smartphone?", "Tracking scans?"]
    f_q = get_font(15)
    for i, q in enumerate(qs):
        col, row = i % 3, i // 3
        x, y = 60 + col * 380, 160 + row * 90
        rounded_rect(draw, (x, y, x + 36, y + 36), radius=18, fill=WHITE)
        draw.text((x + 10, y + 5), str(i + 1), font=get_font(18, bold=True), fill=BRAND_RGB)
        draw.text((x + 56, y + 8), q, font=f_q, fill=WHITE)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-faq-banner.png"), "PNG", optimize=True)


# =============== 主流程 ===============
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp = "scripts/_tmp_agnes"
    os.makedirs(tmp, exist_ok=True)

    print(f"[Agnes 版] 生 4 张医疗主题底图...")
    bases = {}
    for kind in ["hero", "comparison", "scan-demo", "faq-banner"]:
        url = agnes_generate(kind)
        path = f"{tmp}/{kind}.jpg"
        bases[kind] = download(url, path)
        print(f"  → {path}")

    print(f"\n[合成] 4 张配图...")
    make_hero(bases["hero"])
    make_comparison(bases["comparison"])
    make_scan_demo(bases["scan-demo"])
    make_faq_banner(bases["faq-banner"])

    print(f"\n[完成] {OUTPUT_DIR}/")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".png"):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f:50} {sz//1024} KB")


if __name__ == "__main__":
    main()