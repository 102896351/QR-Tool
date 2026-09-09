# -*- coding: utf-8 -*-
"""
通过 GitHub Git Data API 提交源码变更（git 的 HTTPS 通道在当前网络下不可用）。

用法：python push_via_api.py "<commit message>"
只提交源码，不提交 dist/ —— GitHub Actions 会用新源码重新构建并部署。
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

OWNER = "102896351"
REPO = "QR-Tool"
BRANCH = "main"
# 从环境变量读取，禁止把 token 写进文件
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 要提交的路径（相对仓库根）
PATHS = [
    "generate-sitemap.js",
    "index.html",
    "package-lock.json",
    "package.json",
    "public/.nojekyll",
    "public/404.html",
    "public/llms.txt",
    "public/sitemap-0.xml",
    "public/sitemap.xml",
    "scripts/generate-llms.js",
    "scripts/verify-prerender.mjs",
    "src/App.vue",
    "src/blog/posts.json",
    "src/components/AppFooter.vue",
    "src/components/AppHeader.vue",
    "src/components/BlogTeaser.vue",
    "src/components/blog/BlogIndex.vue",
    "src/components/blog/BlogPost.vue",
    "src/components/pages/AboutPage.vue",
    "src/components/pages/ContactPage.vue",
    "src/components/pages/PrivacyPage.vue",
    "src/components/pages/TermsPage.vue",
    "src/composables/useI18n.js",
    "src/composables/useLegal.js",
    "src/composables/usePageHead.js",
    "src/composables/useTab.js",
    "src/config.js",
    "src/main.js",
    "src/router.js",
    "src/views/HomeView.vue",
    "vite.config.js",
]


def req(method, url, data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header("Authorization", f"token {TOKEN}")
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "qr-tool-push")
    if body:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:400]}")
        raise


def main():
    if not TOKEN:
        print("请设置环境变量 GITHUB_TOKEN，例如：")
        print("  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx")
        return 1
    msg = sys.argv[1] if len(sys.argv) > 1 else "chore: update source"
    missing = [p for p in PATHS if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("以下文件不存在，请先检查：")
        for m in missing:
            print("  -", m)
        return 1

    print(f"[1/5] 获取 {BRANCH} 的最新 commit…")
    ref = req("GET", f"{API}/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}")
    base_sha = ref["object"]["sha"]
    commit = req("GET", f"{API}/repos/{OWNER}/{REPO}/git/commits/{base_sha}")
    base_tree = commit["tree"]["sha"]
    print(f"      base commit {base_sha[:8]}  tree {base_tree[:8]}")

    print(f"[2/5] 上传 {len(PATHS)} 个文件的 blob…")
    tree_items = []
    for i, p in enumerate(PATHS, 1):
        full = os.path.join(ROOT, p)
        with open(full, "rb") as f:
            raw = f.read()
        content = base64.b64encode(raw).decode("ascii")
        blob = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/blobs",
                   {"content": content, "encoding": "base64"})
        tree_items.append({"path": p, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print(f"      ({i}/{len(PATHS)}) {p}  {len(raw):,} bytes")

    print("[3/5] 创建 tree…")
    tree = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/trees",
               {"base_tree": base_tree, "tree": tree_items})
    print(f"      tree {tree['sha'][:8]}")

    print("[4/5] 创建 commit…")
    new_commit = req("POST", f"{API}/repos/{OWNER}/{REPO}/git/commits",
                     {"message": msg, "tree": tree["sha"], "parents": [base_sha]})
    print(f"      commit {new_commit['sha'][:8]}")

    print("[5/5] 更新 ref…")
    req("PATCH", f"{API}/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        {"sha": new_commit["sha"]})
    print(f"\n完成：https://github.com/{OWNER}/{REPO}/commit/{new_commit['sha']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
