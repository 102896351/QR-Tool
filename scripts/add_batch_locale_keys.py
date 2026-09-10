"""
为 7 种语言补上 BatchGenerator.vue 需要的 batch.* 文案。

背景：BatchGenerator.vue 的控件文案是中文硬编码，导致英文页上出现
「批量生成 / 内容列表 / 填充示例」等中文，与整站英文 SEO 文案混排。
这里把文案抽到字典里，组件改用 t()。

用法：
  python scripts/add_batch_locale_keys.py --dry-run
  python scripts/add_batch_locale_keys.py
"""
import os
import re
import json
import argparse

LOCALE_DIR = "src/composables/locales"
LANGS = ["en", "zh", "ja", "ko", "fr", "de", "es"]

KEYS = [
    "batch.title", "batch.sub", "batch.label.list", "batch.count.pre",
    "batch.count.post", "batch.placeholder", "batch.action.sample",
    "batch.action.clear", "batch.label.logo", "batch.label.logoScope",
    "batch.label.logoSize", "batch.summary", "batch.summary.total",
    "batch.summary.resolution", "batch.summary.format", "batch.summary.hasLogo",
    "batch.yes", "batch.no", "batch.btn.busy", "batch.btn.zip",
    "batch.note", "batch.err.logoSize", "batch.err.failed",
]

T = {
    "en": {
        "batch.title": "Batch Generate",
        "batch.sub": "One item per line — generate many QR codes at once and download them as a ZIP",
        "batch.label.list": "Content List",
        "batch.count.pre": "",
        "batch.count.post": "items to generate",
        "batch.placeholder": "One item per line, e.g.:\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "Fill sample",
        "batch.action.clear": "Clear",
        "batch.label.logo": "Shared Logo (optional)",
        "batch.label.logoScope": "All QR codes will use the same logo",
        "batch.label.logoSize": "Logo size",
        "batch.summary": "Summary",
        "batch.summary.total": "Total items",
        "batch.summary.resolution": "Resolution per image",
        "batch.summary.format": "Output format",
        "batch.summary.hasLogo": "With logo",
        "batch.yes": "Yes",
        "batch.no": "No",
        "batch.btn.busy": "Packing…",
        "batch.btn.zip": "Generate & Download ZIP",
        "batch.note": "Keep a single batch under <strong>200 items</strong> to avoid browser lag. Everything is generated locally.",
        "batch.err.logoSize": "Logo must be ≤ 2MB",
        "batch.err.failed": "Generation failed: ",
    },
    "zh": {
        "batch.title": "批量生成",
        "batch.sub": "每行一个内容，一次性生成多个二维码并打包为 ZIP",
        "batch.label.list": "内容列表",
        "batch.count.pre": "共",
        "batch.count.post": "个待生成",
        "batch.placeholder": "每行一条内容，例如：\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "填入示例",
        "batch.action.clear": "清空",
        "batch.label.logo": "统一 Logo（可选）",
        "batch.label.logoScope": "所有二维码将使用同一个 Logo",
        "batch.label.logoSize": "Logo 大小",
        "batch.summary": "摘要",
        "batch.summary.total": "总条数",
        "batch.summary.resolution": "单图分辨率",
        "batch.summary.format": "输出格式",
        "batch.summary.hasLogo": "含 Logo",
        "batch.yes": "是",
        "batch.no": "否",
        "batch.btn.busy": "正在打包...",
        "batch.btn.zip": "生成并下载 ZIP",
        "batch.note": "建议单个批次不超过 <strong>200 条</strong>，以免浏览器卡顿。所有内容仅在本地生成。",
        "batch.err.logoSize": "Logo 需 ≤ 2MB",
        "batch.err.failed": "生成失败：",
    },
    "ja": {
        "batch.title": "一括生成",
        "batch.sub": "1行につき1件、まとめてQRコードを生成しZIPでダウンロードできます",
        "batch.label.list": "コンテンツ一覧",
        "batch.count.pre": "計",
        "batch.count.post": "件を生成予定",
        "batch.placeholder": "1行に1件ずつ入力（例）：\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "サンプルを入力",
        "batch.action.clear": "クリア",
        "batch.label.logo": "共通ロゴ（任意）",
        "batch.label.logoScope": "すべてのQRコードで同じロゴを使用します",
        "batch.label.logoSize": "ロゴサイズ",
        "batch.summary": "概要",
        "batch.summary.total": "合計件数",
        "batch.summary.resolution": "1枚あたりの解像度",
        "batch.summary.format": "出力形式",
        "batch.summary.hasLogo": "ロゴあり",
        "batch.yes": "はい",
        "batch.no": "いいえ",
        "batch.btn.busy": "ZIPを作成中...",
        "batch.btn.zip": "生成してZIPをダウンロード",
        "batch.note": "1回の処理は<strong>200件以内</strong>を推奨します。ブラウザが重くなる場合があります。すべてローカルで生成されます。",
        "batch.err.logoSize": "ロゴは2MB以下にしてください",
        "batch.err.failed": "生成に失敗しました：",
    },
    "ko": {
        "batch.title": "일괄 생성",
        "batch.sub": "한 줄에 하나씩 입력하면 여러 QR 코드를 한 번에 만들어 ZIP으로 다운로드합니다",
        "batch.label.list": "콘텐츠 목록",
        "batch.count.pre": "총",
        "batch.count.post": "개 생성 예정",
        "batch.placeholder": "한 줄에 하나씩 입력하세요. 예:\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "예시 채우기",
        "batch.action.clear": "지우기",
        "batch.label.logo": "공통 로고(선택)",
        "batch.label.logoScope": "모든 QR 코드에 동일한 로고가 사용됩니다",
        "batch.label.logoSize": "로고 크기",
        "batch.summary": "요약",
        "batch.summary.total": "총 개수",
        "batch.summary.resolution": "이미지당 해상도",
        "batch.summary.format": "출력 형식",
        "batch.summary.hasLogo": "로고 포함",
        "batch.yes": "예",
        "batch.no": "아니요",
        "batch.btn.busy": "ZIP 생성 중...",
        "batch.btn.zip": "생성 후 ZIP 다운로드",
        "batch.note": "한 번에 <strong>200개 이하</strong>를 권장합니다. 브라우저가 느려질 수 있습니다. 모든 작업은 로컬에서 처리됩니다.",
        "batch.err.logoSize": "로고는 2MB 이하여야 합니다",
        "batch.err.failed": "생성 실패: ",
    },
    "fr": {
        "batch.title": "Génération par lots",
        "batch.sub": "Un élément par ligne — générez plusieurs QR codes d'un coup et téléchargez-les en ZIP",
        "batch.label.list": "Liste des contenus",
        "batch.count.pre": "",
        "batch.count.post": "éléments à générer",
        "batch.placeholder": "Un élément par ligne, par ex. :\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "Remplir un exemple",
        "batch.action.clear": "Effacer",
        "batch.label.logo": "Logo commun (facultatif)",
        "batch.label.logoScope": "Tous les QR codes utiliseront le même logo",
        "batch.label.logoSize": "Taille du logo",
        "batch.summary": "Récapitulatif",
        "batch.summary.total": "Nombre total",
        "batch.summary.resolution": "Résolution par image",
        "batch.summary.format": "Format de sortie",
        "batch.summary.hasLogo": "Avec logo",
        "batch.yes": "Oui",
        "batch.no": "Non",
        "batch.btn.busy": "Création du ZIP...",
        "batch.btn.zip": "Générer et télécharger le ZIP",
        "batch.note": "Limitez un lot à <strong>200 éléments</strong> pour éviter les ralentissements du navigateur. Tout est généré localement.",
        "batch.err.logoSize": "Le logo doit faire ≤ 2 Mo",
        "batch.err.failed": "Échec de la génération : ",
    },
    "de": {
        "batch.title": "Stapelgenerierung",
        "batch.sub": "Ein Eintrag pro Zeile — viele QR-Codes auf einmal erstellen und als ZIP herunterladen",
        "batch.label.list": "Inhaltsliste",
        "batch.count.pre": "",
        "batch.count.post": "Einträge zu erstellen",
        "batch.placeholder": "Ein Eintrag pro Zeile, z. B.:\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "Beispiel einfügen",
        "batch.action.clear": "Leeren",
        "batch.label.logo": "Gemeinsames Logo (optional)",
        "batch.label.logoScope": "Alle QR-Codes verwenden dasselbe Logo",
        "batch.label.logoSize": "Logogröße",
        "batch.summary": "Übersicht",
        "batch.summary.total": "Gesamtanzahl",
        "batch.summary.resolution": "Auflösung pro Bild",
        "batch.summary.format": "Ausgabeformat",
        "batch.summary.hasLogo": "Mit Logo",
        "batch.yes": "Ja",
        "batch.no": "Nein",
        "batch.btn.busy": "ZIP wird erstellt...",
        "batch.btn.zip": "Erstellen und ZIP herunterladen",
        "batch.note": "Bitte maximal <strong>200 Einträge</strong> pro Stapel, um Browser-Verzögerungen zu vermeiden. Alles wird lokal erzeugt.",
        "batch.err.logoSize": "Logo darf ≤ 2 MB sein",
        "batch.err.failed": "Erstellung fehlgeschlagen: ",
    },
    "es": {
        "batch.title": "Generación por lotes",
        "batch.sub": "Un elemento por línea: genera varios códigos QR a la vez y descárgalos en un ZIP",
        "batch.label.list": "Lista de contenidos",
        "batch.count.pre": "",
        "batch.count.post": "elementos por generar",
        "batch.placeholder": "Un elemento por línea, p. ej.:\nhttps://example.com\ntel:+8613800000000",
        "batch.action.sample": "Rellenar ejemplo",
        "batch.action.clear": "Vaciar",
        "batch.label.logo": "Logotipo común (opcional)",
        "batch.label.logoScope": "Todos los códigos QR usarán el mismo logotipo",
        "batch.label.logoSize": "Tamaño del logotipo",
        "batch.summary": "Resumen",
        "batch.summary.total": "Total de elementos",
        "batch.summary.resolution": "Resolución por imagen",
        "batch.summary.format": "Formato de salida",
        "batch.summary.hasLogo": "Con logotipo",
        "batch.yes": "Sí",
        "batch.no": "No",
        "batch.btn.busy": "Empaquetando...",
        "batch.btn.zip": "Generar y descargar ZIP",
        "batch.note": "Se recomienda no superar los <strong>200 elementos</strong> por lote para evitar que el navegador se ralentice. Todo se genera localmente.",
        "batch.err.logoSize": "El logotipo debe ser ≤ 2 MB",
        "batch.err.failed": "Error al generar: ",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for lang in LANGS:
        path = os.path.join(LOCALE_DIR, f"{lang}.js")
        src = open(path, encoding="utf-8").read()
        have = set(re.findall(r'^\s*["\']([A-Za-z0-9_.]+)["\']\s*:', src, re.M))
        todo = [k for k in KEYS if k not in have]
        if not todo:
            print(f"[{lang}] 已存在，跳过")
            continue
        for k in todo:
            assert k in T[lang], f"{lang} 缺 {k} 译文"

        block = ["", "  // === Batch generator (BatchGenerator.vue) ==="]
        for k in todo:
            block.append(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(T[lang][k], ensure_ascii=False)},")
        block_src = "\n".join(block) + "\n"

        idx = src.rfind("}")
        new_src = src[:idx].rstrip("\n") + "\n" + block_src + src[idx:]
        print(f"[{lang}] 补 {len(todo)} 个 batch.* key")
        if args.dry_run:
            print(block_src)
            continue
        open(path, "w", encoding="utf-8", newline="\n").write(new_src)

    if not args.dry_run:
        print("\n[✓] 完成")


if __name__ == "__main__":
    main()
