"""
通用：往 7 个语言字典里批量补 key。

用法：
  python scripts/add_locale_keys.py scripts/locale_additions/theme.json
  python scripts/add_locale_keys.py <payload.json> --dry-run

payload.json 结构（顶层是语言代码，第二层是 key → 文案）：
  {
    "en": { "theme.system": "System" },
    "zh": { "theme.system": "跟随系统" },
    ...
  }

行为：
  - 已存在的 key 跳过（不会覆盖现网文案）
  - 插入到文件末尾的 "}" 之前，带一段分组注释
  - 只对 payload 里出现的语言生效；每个语言的 key 必须齐（防止只翻译一半）
"""
import os
import re
import sys
import json
import argparse

LOCALE_DIR = "src/composables/locales"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("payload", help="JSON 文件路径")
    ap.add_argument("--section", default="补充文案", help="插入的分组注释")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    payload = json.load(open(args.payload, encoding="utf-8"))

    # 校验：每个语言的 key 集合必须一致
    key_sets = {lg: set(v.keys()) for lg, v in payload.items()}
    ref_lang = next(iter(key_sets))
    for lg, ks in key_sets.items():
        diff = key_sets[ref_lang] ^ ks
        assert not diff, f"{lg} 与 {ref_lang} 的 key 不一致：{sorted(diff)}"

    for lang, pairs in payload.items():
        path = os.path.join(LOCALE_DIR, f"{lang}.js")
        if not os.path.exists(path):
            print(f"[{lang}] 跳过：无该语言文件")
            continue
        src = open(path, encoding="utf-8").read()
        have = set(re.findall(r'^\s*["\']([A-Za-z0-9_.]+)["\']\s*:', src, re.M))
        todo = [(k, v) for k, v in pairs.items() if k not in have]
        if not todo:
            print(f"[{lang}] 全部已存在，跳过")
            continue

        block = ["", f"  // === {args.section} ==="]
        for k, v in todo:
            block.append(f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},")
        block_src = "\n".join(block) + "\n"

        idx = src.rfind("}")
        new_src = src[:idx].rstrip("\n") + "\n" + block_src + src[idx:]
        print(f"[{lang}] 补 {len(todo)} 个 key：{', '.join(k for k, _ in todo)}")
        if args.dry_run:
            print(block_src)
            continue
        open(path, "w", encoding="utf-8", newline="\n").write(new_src)

    if not args.dry_run:
        print("\n[✓] 完成")


if __name__ == "__main__":
    main()
