"""
博客配图重生成脚本 —— demo 版本：只做 healthcare 一篇。

风格：
- 用 Picsum（无主题但高质量摄影）做底图，固定 ID 保证可复现
- 全图加品牌色渐变遮罩（统一色调、遮住背景主题不一致）
- 叠加文章特定元素：标题、副标、标签 chip、真二维码示例
- 输出 1200×630 PNG；faq-banner 单独 1200×400
- 修正 example.com → toolbox168.xyz bug

依赖：
  pip install pillow qrcode requests
"""
import io
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =============== 主题配置 ===============
BRAND = "QR Tool Studio"
SITE = "toolbox168.xyz"   # 修正 example.com bug
SLUG = "qr-code-for-healthcare"

# 品牌色（基于 #6366f1 蓝紫）
BRAND_RGB = (99, 102, 241)
BRAND_DARK_RGB = (79, 70, 229)
BRAND_LIGHT_RGB = (199, 210, 254)
TEXT_DARK = (30, 41, 59)
TEXT_MED = (71, 85, 105)
WHITE = (255, 255, 255)
BG_LIGHT = (248, 250, 252)

W, H = 1200, 630
OUTPUT_DIR = f"public/blog/{SLUG}"

# Picsum 固定 ID（保证每次重跑都是同一张图，便于评审）
# 选的是偏干净、对比度强的图，便于叠加文字
PICSUM_HERO = "https://picsum.photos/id/1018/1200/630.jpg"     # 山水（光影强）
PICSUM_COMP = "https://picsum.photos/id/1059/1200/630.jpg"     # 平静水面
PICSUM_SCAN = "https://picsum.photos/id/1031/1200/630.jpg"     # 山脊线
PICSUM_FAQ  = "https://picsum.photos/id/1015/1200/400.jpg"     # 河谷

# =============== 工具函数 ===============
def fetch(url, timeout=30):
    r = requests.get(url, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGB")


def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def gradient_overlay(img, color, direction="left", alpha_start=220, alpha_end=0):
    """在图上叠加品牌色渐变遮罩。"""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for x in range(w):
        if direction == "left":
            t = x / w
        elif direction == "right":
            t = 1 - x / w
        else:  # top
            t = 0
        a = int(alpha_start + (alpha_end - alpha_start) * t)
        for y in range(h):
            overlay.putpixel((x, y), (color[0], color[1], color[2], a))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def solid_overlay(img, color, alpha=200):
    """全图纯色遮罩。"""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (*color, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Pillow 高版本支持的 rounded_rectangle。"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_text_wrapped(draw, text, xy, font, fill, max_width, line_spacing=8):
    """简单换行：按 max_width 自动拆行。"""
    x, y = xy
    lines = []
    cur = ""
    for ch in text:
        candidate = cur + ch
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] > max_width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines):
        draw.text((x, y + i * (font.size + line_spacing)), line, font=font, fill=fill)
    return len(lines)


def make_qr_sample(text, size=180):
    """生成一个真实的二维码示例，返回 PIL Image。"""
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=0)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e293b", back_color="white").convert("RGB")
    return img.resize((size, size), Image.LANCZOS)


def draw_chip(draw, xy, text, font, bg=BRAND_LIGHT_RGB, fg=BRAND_DARK_RGB):
    """画一个圆角标签 chip。"""
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 16, 8
    w = tw + pad_x * 2
    h = th + pad_y * 2
    rounded_rect(draw, (x, y, x + w, y + h), radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return x + w  # 返回 chip 末尾 x，供横向排列


# =============== 4 张图 ===============
def make_hero(base_img):
    """主图：蓝紫渐变覆盖左半边 + 文章标题 + 标签 chip。"""
    img = gradient_overlay(base_img.resize((W, H)), BRAND_RGB, direction="left",
                           alpha_start=235, alpha_end=40)
    draw = ImageDraw.Draw(img)

    # 顶部小标签
    f_label = get_font(18, bold=True)
    draw.text((60, 70), "HEALTHCARE  ·  GUIDE", font=f_label, fill=BRAND_LIGHT_RGB)

    # 大标题（两行）
    f_title = get_font(58, bold=True)
    draw.text((60, 110), "QR Codes in", font=f_title, fill=WHITE)
    draw.text((60, 175), "Healthcare", font=f_title, fill=WHITE)

    # 副标
    f_sub = get_font(22)
    draw.text((60, 260), "7 ways clinics & hospitals", font=f_sub, fill=(224, 231, 255))
    draw.text((60, 290), "use them in 2025", font=f_sub, fill=(224, 231, 255))

    # 4 个 chip
    f_chip = get_font(16, bold=True)
    chip_y = 360
    chip_x = 60
    for tag in ["Patient Intake", "Wayfinding", "Lab Results", "Medication"]:
        chip_x = draw_chip(draw, (chip_x, chip_y), tag, f_chip) + 10

    # 左下角品牌（修 example.com → 真实域名）
    f_brand = get_font(15)
    draw.text((60, H - 45), f"{BRAND}  ·  {SITE}", font=f_brand, fill=(199, 210, 254))

    # 右下角加一个真二维码示例（白色圆角背景框）
    qr_img = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=170)
    qr_bg = Image.new("RGBA", (qr_img.size[0] + 24, qr_img.size[1] + 24),
                      (255, 255, 255, 255))
    qr_bg.paste(qr_img, (12, 12))
    # 加阴影
    shadow = Image.new("RGBA", qr_bg.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((4, 6, qr_bg.size[0] - 1, qr_bg.size[1] - 1),
                         radius=12, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img.paste(shadow, (W - qr_bg.size[0] - 60 + 4, H - qr_bg.size[1] - 50 + 6), shadow)
    img.paste(qr_bg, (W - qr_bg.size[0] - 60, H - qr_bg.size[1] - 50))

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-hero.png"), "PNG", optimize=True)


def make_comparison(base_img):
    """对比图：浅色遮罩 + Before/After 对比卡片。"""
    img = solid_overlay(base_img.resize((W, H)), BG_LIGHT, alpha=210)
    draw = ImageDraw.Draw(img)

    # 顶部品牌条
    draw.rectangle((0, 0, W, 6), fill=BRAND_RGB)

    f_title = get_font(36, bold=True)
    f_sub = get_font(18)
    draw.text((60, 50), "Paper Intake vs QR Intake", font=f_title, fill=TEXT_DARK)
    draw.text((60, 100), "Same clinic. Same patient. Different result.",
              font=f_sub, fill=TEXT_MED)

    # 左边卡片（Before - 黄色纸张风）
    card1 = (60, 170, 580, 540)
    rounded_rect(draw, card1, radius=20, fill=WHITE, outline=(226, 232, 240), width=2)
    draw.text((90, 195), "BEFORE", font=get_font(20, bold=True), fill=(220, 38, 38))
    draw.text((90, 235), "Paper Clipboard", font=get_font(24, bold=True), fill=TEXT_DARK)
    # 画一叠纸
    paper_x, paper_y = 90, 290
    for i in range(5):
        rounded_rect(draw, (paper_x + i * 4, paper_y + i * 4,
                            paper_x + 380 + i * 4, paper_y + 200 + i * 4),
                     radius=4, fill=(254, 240, 138), outline=(202, 138, 4), width=2)
    for line_i in range(4):
        y = paper_y + 40 + line_i * 28
        draw.line([(paper_x + 20, y), (paper_x + 360, y)], fill=(202, 138, 4), width=3)
    draw.text((paper_x, paper_y + 220), "10 min", font=get_font(36, bold=True), fill=(220, 38, 38))
    draw.text((paper_x + 130, paper_y + 232), "per patient", font=get_font(16), fill=TEXT_MED)

    # 右边卡片（After - 蓝色二维码风）
    card2 = (620, 170, W - 60, 540)
    rounded_rect(draw, card2, radius=20, fill=(220, 252, 231), outline=(34, 197, 94), width=2)
    draw.text((650, 195), "AFTER", font=get_font(20, bold=True), fill=(22, 163, 74))
    draw.text((650, 235), "QR Code Check-in", font=get_font(24, bold=True), fill=TEXT_DARK)

    # 画手机 + 二维码
    phone_x, phone_y = 700, 290
    phone_w, phone_h = 200, 240
    rounded_rect(draw, (phone_x, phone_y, phone_x + phone_w, phone_y + phone_h),
                 radius=24, fill=(30, 41, 59))
    rounded_rect(draw, (phone_x + 10, phone_y + 20,
                        phone_x + phone_w - 10, phone_y + phone_h - 30),
                 radius=8, fill=(248, 250, 252))
    # 内嵌二维码
    inner_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=150)
    img.paste(inner_qr, (phone_x + 25, phone_y + 35))
    # 绿色 check 标识
    check_x = phone_x + phone_w - 50
    check_y = phone_y + phone_h - 70
    rounded_rect(draw, (check_x, check_y, check_x + 36, check_y + 36),
                 radius=18, fill=(22, 163, 74))
    draw.text((check_x + 11, check_y + 6), "✓", font=get_font(20, bold=True), fill=WHITE)
    draw.text((650, phone_y + phone_h + 10), "90 sec", font=get_font(36, bold=True), fill=(22, 163, 74))
    draw.text((780, phone_y + phone_h + 22), "per patient", font=get_font(16), fill=TEXT_MED)

    # 底部金句
    f_kicker = get_font(15, bold=True)
    draw.text((W // 2, H - 50), "Saves 8 min per patient  ·  2.5 kg less paper per day  ·  88% patient open rate",
              font=f_kicker, fill=BRAND_DARK_RGB, anchor="mm")

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-comparison.png"), "PNG", optimize=True)


def make_scan_demo(base_img):
    """扫描演示图：药瓶 + 箭头 + 手机验证的视觉。"""
    img = solid_overlay(base_img.resize((W, H)), (240, 249, 255), alpha=215)
    draw = ImageDraw.Draw(img)

    # 标题
    f_title = get_font(32, bold=True)
    f_sub = get_font(17)
    draw.text((60, 50), "Patient scans QR on prescription label", font=f_title, fill=TEXT_DARK)
    draw.text((60, 95), "Verified medication, dose, and refill status — no app, no signup.",
              font=f_sub, fill=TEXT_MED)

    # 左侧：药瓶/处方签
    rx_x, rx_y = 100, 170
    rx_w, rx_h = 280, 380
    rounded_rect(draw, (rx_x, rx_y, rx_x + rx_w, rx_y + rx_h),
                 radius=16, fill=WHITE, outline=(226, 232, 240), width=2)
    # 顶部蓝色条
    rounded_rect(draw, (rx_x + 20, rx_y + 20, rx_x + rx_w - 20, rx_y + 80),
                 radius=8, fill=(59, 130, 246))
    # 药签
    rounded_rect(draw, (rx_x + 20, rx_y + 100, rx_x + rx_w - 20, rx_y + 220),
                 radius=8, fill=(254, 240, 138))
    draw.text((rx_x + 35, rx_y + 115), "Amoxicillin 500mg", font=get_font(16, bold=True), fill=TEXT_DARK)
    draw.text((rx_x + 35, rx_y + 145), "Take 1 cap, 3x daily", font=get_font(13), fill=TEXT_DARK)
    draw.text((rx_x + 35, rx_y + 168), "Rx #847291", font=get_font(12), fill=TEXT_MED)
    # 内嵌二维码
    rx_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=120)
    img.paste(rx_qr, (rx_x + 80, rx_y + 230))

    # 中间：箭头
    arrow_y = rx_y + 180
    draw.line([(rx_x + rx_w + 30, arrow_y), (rx_x + rx_w + 130, arrow_y)],
              fill=BRAND_RGB, width=6)
    # 箭头头部
    draw.polygon([(rx_x + rx_w + 130, arrow_y - 12),
                  (rx_x + rx_w + 160, arrow_y),
                  (rx_x + rx_w + 130, arrow_y + 12)], fill=BRAND_RGB)

    # 右侧：手机 + 扫描界面
    ph_x, ph_y = 580, 160
    ph_w, ph_h = 220, 400
    rounded_rect(draw, (ph_x, ph_y, ph_x + ph_w, ph_y + ph_h),
                 radius=28, fill=(15, 23, 42))
    # 屏幕
    rounded_rect(draw, (ph_x + 12, ph_y + 30, ph_x + ph_w - 12, ph_y + ph_h - 40),
                 radius=10, fill=(241, 245, 249))
    # 取景框 + 二维码
    fx = ph_x + 50
    fy = ph_y + 80
    rounded_rect(draw, (fx, fy, fx + 120, fy + 120), radius=6,
                 outline=(34, 197, 94), width=4)
    phone_qr = make_qr_sample(f"https://{SITE}/blog/{SLUG}/", size=90)
    img.paste(phone_qr, (fx + 15, fy + 15))
    # verified 标识
    vb_x = ph_x + 75
    vb_y = ph_y + 230
    rounded_rect(draw, (vb_x, vb_y, vb_x + 70, vb_y + 70), radius=35, fill=(22, 163, 74))
    draw.text((vb_x + 28, vb_y + 18), "✓", font=get_font(40, bold=True), fill=WHITE)
    draw.text((ph_x + ph_w // 2, vb_y + 80), "Verified", font=get_font(16, bold=True),
              fill=(22, 163, 74), anchor="mm")

    # 右下角：完成态
    right_x = ph_x + ph_w + 50
    rounded_rect(draw, (right_x, arrow_y - 60, right_x + 100, arrow_y + 60),
                 radius=12, outline=BRAND_RGB, width=3)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-scan-demo.png"), "PNG", optimize=True)


def make_faq_banner(base_img):
    """问答 banner：1200×400，强蓝色遮罩 + 6 问答。"""
    BW, BH = 1200, 400
    img = gradient_overlay(base_img.resize((BW, BH)), BRAND_RGB, direction="top",
                           alpha_start=235, alpha_end=180)
    draw = ImageDraw.Draw(img)

    f_title = get_font(30, bold=True)
    f_sub = get_font(16)
    draw.text((60, 40), "6 Questions About QR Codes in Healthcare", font=f_title, fill=WHITE)
    draw.text((60, 80), "The answers patients and clinic staff ask most", font=f_sub, fill=BRAND_LIGHT_RGB)

    qs = [
        "HIPAA compliant?",
        "What size?",
        "Static or dynamic?",
        "Infection risk?",
        "No smartphone?",
        "Tracking scans?",
    ]
    f_q = get_font(15)
    for i, q in enumerate(qs):
        col = i % 3
        row = i // 3
        x = 60 + col * 380
        y = 160 + row * 90
        # 圆形数字
        rounded_rect(draw, (x, y, x + 36, y + 36), radius=18, fill=WHITE)
        draw.text((x + 10, y + 5), str(i + 1), font=get_font(18, bold=True), fill=BRAND_RGB)
        # 问题
        draw.text((x + 56, y + 8), q, font=f_q, fill=WHITE)

    img.convert("RGB").save(os.path.join(OUTPUT_DIR, f"{SLUG}-faq-banner.png"), "PNG", optimize=True)


# =============== 主流程 ===============
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[demo] 拉取 4 张底图...")
    hero = fetch(PICSUM_HERO)
    comp = fetch(PICSUM_COMP)
    scan = fetch(PICSUM_SCAN)
    faq = fetch(PICSUM_FAQ)
    print(f"[demo] 合成 hero ...")
    make_hero(hero)
    print(f"[demo] 合成 comparison ...")
    make_comparison(comp)
    print(f"[demo] 合成 scan-demo ...")
    make_scan_demo(scan)
    print(f"[demo] 合成 faq-banner ...")
    make_faq_banner(faq)
    print(f"[demo] 完成 → {OUTPUT_DIR}/")
    for f in ["hero.png", "comparison.png", "scan-demo.png", "faq-banner.png"]:
        # 老文件命名约定是带 slug 前缀，但产物是 {slug}-{kind}.png；
        # 这里同时落两份以兼容旧路径
        pass


if __name__ == "__main__":
    main()