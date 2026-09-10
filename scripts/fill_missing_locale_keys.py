"""
补齐 ja / ko / fr / de / es 字典中缺失的 39 个 key。

缺失原因：早期只给 en / zh 写了这批文案（矩阵样式名、场景标签、FAQ、配色预设），
其余 5 种语言直接用 key 字面量渲染（页面上会显示 "gen.dots.classy" 这种东西）。

用法：
  python scripts/fill_missing_locale_keys.py --dry-run
  python scripts/fill_missing_locale_keys.py
"""
import os
import re
import json
import argparse

LOCALE_DIR = "src/composables/locales"
LANGS = ["ja", "ko", "fr", "de", "es"]

# === 翻译表 ===
T = {
    "ja": {
        "gen.dots.square": "クラシック四角",
        "gen.dots.dots": "リキッドドット",
        "gen.dots.rounded": "角丸四角",
        "gen.dots.classy": "クラシー",
        "gen.dots.classyRounded": "クラシー角丸",
        "gen.dots.extraRounded": "強角丸",
        "gen.corners.square": "四角",
        "gen.corners.dot": "丸点",
        "gen.corners.extraRounded": "角丸四角",
        "gen.corners.classy": "クラシーライン",
        "gen.corners.classyRounded": "角丸ライン",
        "preset.brand": "ブランドグラデーション",
        "preset.mono": "モノクロ",
        "preset.sunshine": "サニーデイ",
        "preset.forest": "フォレスト",
        "preset.cherry": "桜",
        "preset.deepsea": "ディープシー",
        "mkt.useCases.1.tag": "マーケティング",
        "mkt.useCases.2.tag": "ビジネス",
        "mkt.useCases.3.tag": "飲食",
        "mkt.useCases.4.tag": "小売",
        "mkt.useCases.5.tag": "イベント",
        "mkt.useCases.6.tag": "教育",
        "faq.q1": "QRコードとは何ですか？",
        "faq.a1": "QRコード（Quick Response Code）は、1994年にデンソーウェーブが発明した二次元バーコードです。URL、テキスト、連絡先、WiFiパスワードなどを格納できます。一次元バーコードに比べて大容量・高耐性・高速読み取りが可能で、モバイル決済、商品トレーサビリティ、マーケティングなど幅広く使われています。",
        "faq.q2": "QRコード生成は無料ですか？",
        "faq.a2": "はい、QR Tool Studio は完全無料で隠れた課金はありません。カスタムカラー、グラデーション、ロゴ、一括生成、マルチフォーマット書き出しなどすべての機能が無料で、登録も不要です。",
        "faq.q3": "QRコードに有効期限はありますか？ずっと使えますか？",
        "faq.a3": "いいえ。当ツールは静的QRコードを生成します。一度作成すれば永久に有効で、読み取り回数の制限もなく、サーバー停止で使えなくなることもありません。PNGまたはSVGでダウンロードし、バックアップを保管することをおすすめします。",
        "faq.q4": "入力した内容はサーバーに送信されますか？",
        "faq.a4": "いいえ、一切送信されません。QRコードの生成・描画・ダウンロードはすべてブラウザ内で完結します。内容がサーバーにアップロードされることはありません。ページを閉じれば、ご自身で保存したLocalStorageの履歴以外は何も残りません。",
        "faq.q5": "どの種類のQRコードに対応していますか？",
        "faq.a5": "URL、vCard、プレーンテキスト、メール（mailto:）、電話（tel:）、SMS（sms:）、WiFi自動接続、位置情報の8種類に対応しています。任意の文字列をそのまま貼り付けることもできます。",
        "faq.q6": "中央に自分のロゴを入れられますか？",
        "faq.a6": "はい。PNG / JPG / SVG のロゴ画像（最大2MB）に対応しています。ロゴサイズは10%〜50%で調整可能です。読み取り成功率を保つため、誤り訂正レベルをH（30%）に設定することをおすすめします。",
        "faq.q7": "QRコードは白黒でなければいけませんか？",
        "faq.a7": "必ずしもそうではありません。任意の前景色のほか、2色の線形・放射グラデーション（6種のスタイルプリセット）に対応しています。読み取り率を高めるには、コントラストを高く保ち（濃い前景＋明るい背景）、反転配色は避けてください。",
        "faq.q8": "どの書き出し形式に対応していますか？",
        "faq.a8": "PNG（1024×1024の高解像度ビットマップ、SNS共有に最適）、SVG（ベクター、印刷や大判ポスターでも劣化なし）、JPEG（圧縮ビットマップ、メール添付向け）の3形式に対応しています。ワンクリックで画像をクリップボードにコピーすることもできます。",
    },
    "ko": {
        "gen.dots.square": "클래식 사각",
        "gen.dots.dots": "리퀴드 도트",
        "gen.dots.rounded": "둥근 사각",
        "gen.dots.classy": "클래시",
        "gen.dots.classyRounded": "클래시 둥근",
        "gen.dots.extraRounded": "엑스트라 둥근",
        "gen.corners.square": "사각",
        "gen.corners.dot": "원형 점",
        "gen.corners.extraRounded": "둥근 사각",
        "gen.corners.classy": "클래시 라인",
        "gen.corners.classyRounded": "둥근 라인",
        "preset.brand": "브랜드 그라데이션",
        "preset.mono": "순수 흑백",
        "preset.sunshine": "화창한 날",
        "preset.forest": "포레스트",
        "preset.cherry": "벚꽃",
        "preset.deepsea": "딥 씨",
        "mkt.useCases.1.tag": "마케팅",
        "mkt.useCases.2.tag": "비즈니스",
        "mkt.useCases.3.tag": "요식업",
        "mkt.useCases.4.tag": "리테일",
        "mkt.useCases.5.tag": "이벤트",
        "mkt.useCases.6.tag": "교육",
        "faq.q1": "QR 코드란 무엇인가요?",
        "faq.a1": "QR 코드(Quick Response Code)는 1994년 덴소웨이브가 발명한 2차원 바코드입니다. URL, 텍스트, 연락처, WiFi 비밀번호 등을 저장할 수 있습니다. 1차원 바코드보다 용량이 크고 오류에 강하며 인식 속도가 빨라 모바일 결제, 제품 이력 추적, 마케팅 등에 널리 쓰입니다.",
        "faq.q2": "QR 코드 생성기는 무료인가요?",
        "faq.a2": "네, QR Tool Studio는 숨은 비용 없이 완전 무료입니다. 사용자 지정 색상, 그라데이션, 로고, 일괄 생성, 다중 포맷 내보내기 등 모든 기능이 무료이며 회원가입도 필요 없습니다.",
        "faq.q3": "QR 코드에 만료 기한이 있나요? 계속 사용할 수 있나요?",
        "faq.a3": "아니요. 저희는 정적 QR 코드를 생성합니다. 한 번 만들면 영구적으로 사용할 수 있고 스캔 횟수 제한도 없으며 서버 장애로 작동이 멈추지도 않습니다. PNG 또는 SVG로 다운로드해 백업해 두시길 권장합니다.",
        "faq.q4": "입력한 내용이 서버로 전송되나요?",
        "faq.a4": "전혀 아닙니다. QR 코드 생성, 렌더링, 다운로드는 모두 브라우저 안에서 이루어집니다. 내용은 어떤 서버에도 업로드되지 않습니다. 페이지를 닫으면 직접 저장한 LocalStorage 기록 외에는 아무것도 남지 않습니다.",
        "faq.q5": "어떤 종류의 QR 코드를 지원하나요?",
        "faq.a5": "URL, vCard, 일반 텍스트, 이메일(mailto:), 전화(tel:), SMS(sms:), WiFi 자동 연결, 위치 좌표 등 8가지 유형을 지원합니다. 임의의 문자열을 그대로 붙여넣을 수도 있습니다.",
        "faq.q6": "가운데에 제 로고를 넣을 수 있나요?",
        "faq.a6": "네. PNG / JPG / SVG 로고 이미지를 최대 2MB까지 지원합니다. 로고 크기는 10%~50% 사이에서 조절할 수 있습니다. 스캔 성공률을 위해 오류 정정 레벨을 H(30%)로 설정하시길 권장합니다.",
        "faq.q7": "QR 코드는 반드시 흑백이어야 하나요?",
        "faq.a7": "꼭 그렇지는 않습니다. 모든 전경색을 지원하며, 2색 선형·방사형 그라데이션과 6가지 스타일 프리셋도 제공합니다. 스캔률을 높이려면 대비를 크게 유지하고(어두운 전경 + 밝은 배경) 반전 색상은 피하세요.",
        "faq.q8": "어떤 내보내기 형식을 지원하나요?",
        "faq.a8": "PNG(1024×1024 고해상도 비트맵, SNS 공유에 최적), SVG(벡터, 인쇄 및 대형 포스터에서 무손실 확대), JPEG(압축 비트맵, 이메일 첨부용) 3가지 형식을 지원합니다. 클릭 한 번으로 이미지를 클립보드에 복사할 수도 있습니다.",
    },
    "fr": {
        "gen.dots.square": "Carré classique",
        "gen.dots.dots": "Points liquides",
        "gen.dots.rounded": "Carré arrondi",
        "gen.dots.classy": "Élégant",
        "gen.dots.classyRounded": "Élégant arrondi",
        "gen.dots.extraRounded": "Très arrondi",
        "gen.corners.square": "Carré",
        "gen.corners.dot": "Point plein",
        "gen.corners.extraRounded": "Carré arrondi",
        "gen.corners.classy": "Ligne élégante",
        "gen.corners.classyRounded": "Ligne arrondie",
        "preset.brand": "Dégradé de marque",
        "preset.mono": "Noir et blanc pur",
        "preset.sunshine": "Jour ensoleillé",
        "preset.forest": "Forêt fraîche",
        "preset.cherry": "Fleur de cerisier",
        "preset.deepsea": "Grand bleu",
        "mkt.useCases.1.tag": "Marketing",
        "mkt.useCases.2.tag": "Entreprise",
        "mkt.useCases.3.tag": "Restauration",
        "mkt.useCases.4.tag": "Commerce",
        "mkt.useCases.5.tag": "Événementiel",
        "mkt.useCases.6.tag": "Éducation",
        "faq.q1": "Qu'est-ce qu'un QR code ?",
        "faq.a1": "Un QR code (Quick Response Code) est un code-barres bidimensionnel inventé par Denso Wave en 1994. Il peut stocker des URL, du texte, des cartes de visite, des mots de passe WiFi, etc. Par rapport aux codes-barres 1D, il offre une capacité supérieure, une meilleure tolérance aux erreurs et un scan plus rapide — largement utilisé pour les paiements mobiles, la traçabilité des produits et le marketing.",
        "faq.q2": "Le générateur de QR code est-il gratuit ?",
        "faq.a2": "Oui, QR Tool Studio est entièrement gratuit, sans frais cachés. Toutes les fonctionnalités (couleurs personnalisées, dégradés, logo, génération par lots, export multi-format) sont gratuites et aucune inscription n'est requise.",
        "faq.q3": "Le QR code expire-t-il ? Puis-je l'utiliser définitivement ?",
        "faq.a3": "Non. Nous générons des QR codes statiques — une fois créés, ils fonctionnent indéfiniment, sans limite de scans et sans risque de panne liée à un serveur. Nous recommandons de télécharger en PNG ou SVG et de conserver une sauvegarde.",
        "faq.q4": "Mon contenu sera-t-il envoyé à un serveur ?",
        "faq.a4": "Absolument pas. La génération, le rendu et le téléchargement des QR codes se font entièrement dans votre navigateur. Le contenu n'est jamais envoyé à un serveur. Après avoir fermé la page, il ne reste aucune trace, hormis l'historique LocalStorage que vous avez enregistré vous-même.",
        "faq.q5": "Quels types de QR codes sont pris en charge ?",
        "faq.a5": "Nous prenons en charge 8 types courants : URL, vCard, texte brut, e-mail (mailto:), téléphone (tel:), SMS (sms:), connexion WiFi automatique et coordonnées géographiques. Vous pouvez aussi coller n'importe quelle chaîne directement.",
        "faq.q6": "Puis-je insérer mon propre logo au centre ?",
        "faq.a6": "Oui. Nous acceptons les logos PNG / JPG / SVG jusqu'à 2 Mo. La taille du logo est réglable entre 10 % et 50 %. Nous recommandons de régler la correction d'erreur sur H (30 %) pour garantir la lecture.",
        "faq.q7": "Les QR codes doivent-ils être en noir et blanc ?",
        "faq.a7": "Pas nécessairement. Cet outil accepte n'importe quelle couleur de premier plan, ainsi que des dégradés linéaires / radiaux bicolores avec 6 préréglages. Pour un meilleur taux de lecture, gardez un fort contraste (premier plan sombre + fond clair) et évitez les couleurs inversées.",
        "faq.q8": "Quels formats d'export sont pris en charge ?",
        "faq.a8": "Trois formats sont disponibles : PNG (bitmap haute résolution 1024×1024, idéal pour le partage social), SVG (vectoriel, mise à l'échelle sans perte pour l'impression et les grands posters), JPEG (bitmap compressé pour les pièces jointes). Vous pouvez aussi copier l'image dans le presse-papiers en un clic.",
    },
    "de": {
        "gen.dots.square": "Klassisch eckig",
        "gen.dots.dots": "Flüssige Punkte",
        "gen.dots.rounded": "Abgerundetes Quadrat",
        "gen.dots.classy": "Elegant",
        "gen.dots.classyRounded": "Elegant abgerundet",
        "gen.dots.extraRounded": "Stark abgerundet",
        "gen.corners.square": "Quadrat",
        "gen.corners.dot": "Voller Punkt",
        "gen.corners.extraRounded": "Abgerundetes Quadrat",
        "gen.corners.classy": "Elegante Linie",
        "gen.corners.classyRounded": "Abgerundete Linie",
        "preset.brand": "Marken-Verlauf",
        "preset.mono": "Reines Schwarz-Weiß",
        "preset.sunshine": "Sonniger Tag",
        "preset.forest": "Frischer Wald",
        "preset.cherry": "Kirschblüte",
        "preset.deepsea": "Tiefsee",
        "mkt.useCases.1.tag": "Marketing",
        "mkt.useCases.2.tag": "Business",
        "mkt.useCases.3.tag": "Gastronomie",
        "mkt.useCases.4.tag": "Handel",
        "mkt.useCases.5.tag": "Events",
        "mkt.useCases.6.tag": "Bildung",
        "faq.q1": "Was ist ein QR-Code?",
        "faq.a1": "Ein QR-Code (Quick Response Code) ist ein zweidimensionaler Barcode, der 1994 von Denso Wave erfunden wurde. Er kann URLs, Text, Visitenkarten, WLAN-Passwörter und mehr speichern. Im Vergleich zu 1D-Barcodes bietet er höhere Kapazität, bessere Fehlertoleranz und schnelleres Scannen — weit verbreitet bei mobilen Zahlungen, Produktrückverfolgung und Marketing.",
        "faq.q2": "Ist der QR-Code-Generator kostenlos?",
        "faq.a2": "Ja, QR Tool Studio ist völlig kostenlos, ohne versteckte Gebühren. Alle Funktionen (eigene Farben, Verläufe, Logo, Stapelgenerierung, Export in mehreren Formaten) sind kostenlos und keine Registrierung erforderlich.",
        "faq.q3": "Läuft der QR-Code ab? Kann ich ihn dauerhaft nutzen?",
        "faq.a3": "Nein. Wir erzeugen statische QR-Codes — einmal erstellt, funktionieren sie dauerhaft, ohne Scan-Limit und ohne Ausfall, falls ein Server nicht erreichbar ist. Wir empfehlen den Download als PNG oder SVG und eine Sicherungskopie.",
        "faq.q4": "Werden meine Inhalte auf einen Server hochgeladen?",
        "faq.a4": "Absolut nicht. Erstellung, Rendering und Download der QR-Codes erfolgen vollständig lokal in Ihrem Browser. Inhalte werden niemals auf einen Server hochgeladen. Nach dem Schließen der Seite bleibt nichts zurück außer dem LocalStorage-Verlauf, den Sie selbst gespeichert haben.",
        "faq.q5": "Welche QR-Code-Typen werden unterstützt?",
        "faq.a5": "Wir unterstützen 8 gängige Typen: URL, vCard, Klartext, E-Mail (mailto:), Telefon (tel:), SMS (sms:), automatische WLAN-Verbindung und Geokoordinaten. Sie können auch jede beliebige Zeichenfolge direkt einfügen.",
        "faq.q6": "Kann ich mein eigenes Logo in die Mitte setzen?",
        "faq.a6": "Ja. Wir unterstützen Logo-Bilder im Format PNG / JPG / SVG bis 2 MB. Die Logogröße lässt sich zwischen 10 % und 50 % einstellen. Für eine sichere Erkennung empfehlen wir Fehlerkorrektur H (30 %).",
        "faq.q7": "Müssen QR-Codes schwarz-weiß sein?",
        "faq.a7": "Nicht unbedingt. Dieses Tool unterstützt jede Vordergrundfarbe sowie zweifarbige lineare / radiale Verläufe mit 6 Stilvorlagen. Für die beste Scanrate sorgen Sie für hohen Kontrast (dunkler Vordergrund + heller Hintergrund) und vermeiden invertierte Farben.",
        "faq.q8": "Welche Exportformate werden unterstützt?",
        "faq.a8": "Drei Formate werden unterstützt: PNG (hochauflösende Bitmap 1024×1024, ideal für Social Media), SVG (Vektor, verlustfreie Skalierung für Druck und große Poster), JPEG (komprimierte Bitmap für E-Mail-Anhänge). Sie können das Bild auch mit einem Klick in die Zwischenablage kopieren.",
    },
    "es": {
        "gen.dots.square": "Cuadrado clásico",
        "gen.dots.dots": "Puntos líquidos",
        "gen.dots.rounded": "Cuadrado redondeado",
        "gen.dots.classy": "Elegante",
        "gen.dots.classyRounded": "Elegante redondeado",
        "gen.dots.extraRounded": "Muy redondeado",
        "gen.corners.square": "Cuadrado",
        "gen.corners.dot": "Punto sólido",
        "gen.corners.extraRounded": "Cuadrado redondeado",
        "gen.corners.classy": "Línea elegante",
        "gen.corners.classyRounded": "Línea redondeada",
        "preset.brand": "Degradado de marca",
        "preset.mono": "Blanco y negro puro",
        "preset.sunshine": "Día soleado",
        "preset.forest": "Bosque fresco",
        "preset.cherry": "Flor de cerezo",
        "preset.deepsea": "Mar profundo",
        "mkt.useCases.1.tag": "Marketing",
        "mkt.useCases.2.tag": "Empresas",
        "mkt.useCases.3.tag": "Restauración",
        "mkt.useCases.4.tag": "Comercio",
        "mkt.useCases.5.tag": "Eventos",
        "mkt.useCases.6.tag": "Educación",
        "faq.q1": "¿Qué es un código QR?",
        "faq.a1": "Un código QR (Quick Response Code) es un código de barras bidimensional inventado por Denso Wave en 1994. Puede almacenar URL, texto, tarjetas de contacto, contraseñas de WiFi y más. Frente a los códigos de barras 1D, ofrece mayor capacidad, mejor tolerancia a errores y un escaneo más rápido: se usa ampliamente en pagos móviles, trazabilidad de productos y marketing.",
        "faq.q2": "¿El generador de códigos QR es gratis?",
        "faq.a2": "Sí, QR Tool Studio es totalmente gratuito y sin cargos ocultos. Todas las funciones (colores personalizados, degradados, logotipo, generación por lotes, exportación multiformato) son gratuitas y no se requiere registro.",
        "faq.q3": "¿El código QR caduca? ¿Puedo usarlo para siempre?",
        "faq.a3": "No. Generamos códigos QR estáticos: una vez creados funcionan para siempre, sin límite de escaneos y sin dejar de funcionar si algún servidor se cae. Recomendamos descargarlo en PNG o SVG y guardar una copia de seguridad.",
        "faq.q4": "¿Mi contenido se sube a un servidor?",
        "faq.a4": "En absoluto. La generación, el renderizado y la descarga de los códigos QR ocurren por completo en tu navegador. El contenido nunca se sube a ningún servidor. Al cerrar la página no queda ningún rastro, salvo el historial de LocalStorage que hayas guardado tú mismo.",
        "faq.q5": "¿Qué tipos de códigos QR son compatibles?",
        "faq.a5": "Admitimos 8 tipos habituales: URL, vCard, texto plano, correo (mailto:), teléfono (tel:), SMS (sms:), conexión WiFi automática y coordenadas geográficas. También puedes pegar cualquier cadena directamente.",
        "faq.q6": "¿Puedo poner mi propio logotipo en el centro?",
        "faq.a6": "Sí. Admitimos logotipos en PNG / JPG / SVG de hasta 2 MB. El tamaño del logotipo se puede ajustar entre el 10 % y el 50 %. Recomendamos usar corrección de errores H (30 %) para asegurar el escaneo.",
        "faq.q7": "¿Los códigos QR tienen que ser en blanco y negro?",
        "faq.a7": "No necesariamente. Esta herramienta admite cualquier color de primer plano, además de degradados lineales / radiales de dos colores con 6 estilos predefinidos. Para una mejor tasa de lectura, mantén un alto contraste (primer plano oscuro + fondo claro) y evita los colores invertidos.",
        "faq.q8": "¿Qué formatos de exportación se admiten?",
        "faq.a8": "Se admiten tres formatos: PNG (mapa de bits de alta resolución 1024×1024, ideal para compartir en redes), SVG (vectorial, escalado sin pérdida para impresión y carteles grandes), JPEG (mapa de bits comprimido para adjuntos de correo). También puedes copiar la imagen al portapapeles con un clic.",
    },
}

# 输出顺序：按 en.js 里的分组顺序排，便于人工比对
ORDER = [
    "gen.dots.square", "gen.dots.dots", "gen.dots.rounded", "gen.dots.classy",
    "gen.dots.classyRounded", "gen.dots.extraRounded",
    "gen.corners.square", "gen.corners.dot", "gen.corners.extraRounded",
    "gen.corners.classy", "gen.corners.classyRounded",
    "preset.brand", "preset.mono", "preset.sunshine", "preset.forest",
    "preset.cherry", "preset.deepsea",
    "mkt.useCases.1.tag", "mkt.useCases.2.tag", "mkt.useCases.3.tag",
    "mkt.useCases.4.tag", "mkt.useCases.5.tag", "mkt.useCases.6.tag",
    "faq.q1", "faq.a1", "faq.q2", "faq.a2", "faq.q3", "faq.a3", "faq.q4", "faq.a4",
    "faq.q5", "faq.a5", "faq.q6", "faq.a6", "faq.q7", "faq.a7", "faq.q8", "faq.a8",
]


def key_set(src):
    return set(re.findall(r'^\s*["\']([A-Za-z0-9_.]+)["\']\s*:', src, re.M))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    en_src = open(os.path.join(LOCALE_DIR, "en.js"), encoding="utf-8").read()
    en_keys = key_set(en_src)

    for lang in LANGS:
        path = os.path.join(LOCALE_DIR, f"{lang}.js")
        src = open(path, encoding="utf-8").read()
        have = key_set(src)
        missing = [k for k in ORDER if k not in have]
        # 校验：表里的 key 必须真实存在于 en，且本次要补的都在表里
        for k in missing:
            assert k in en_keys, f"{k} 不存在于 en.js"
            assert k in T[lang], f"{lang} 缺少 {k} 的译文"
        if not missing:
            print(f"[{lang}] 无需补全")
            continue

        block = ["", "  // === 补齐：矩阵样式名 / 场景标签 / FAQ / 配色预设 ==="]
        for k in missing:
            block.append(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(T[lang][k], ensure_ascii=False)},")
        block_src = "\n".join(block) + "\n"

        idx = src.rfind("}")
        new_src = src[:idx].rstrip("\n") + "\n" + block_src + src[idx:]

        print(f"[{lang}] 补 {len(missing)} 个 key")
        if args.dry_run:
            print(block_src)
            continue
        open(path, "w", encoding="utf-8", newline="\n").write(new_src)

    if not args.dry_run:
        print("\n[✓] 完成，校验：")
        for lang in LANGS:
            src = open(os.path.join(LOCALE_DIR, f"{lang}.js"), encoding="utf-8").read()
            miss = en_keys - key_set(src)
            print(f"  {lang}: 仍缺 {len(miss)} 个" + (f" {sorted(miss)[:8]}" if miss else ""))


if __name__ == "__main__":
    main()
