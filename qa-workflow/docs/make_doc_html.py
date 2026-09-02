# -*- coding: utf-8 -*-
"""markdown → 自包含单文件 HTML（内嵌 CSS，无 CDN，内网可开）。
用法：python make_doc_html.py <输入.md> <输出.html>"""
import sys
from pathlib import Path

import markdown

CSS = """
:root { --ink:#1f2933; --accent:#0b6e4f; --line:#e4e7eb; --bg:#f8f9fa; }
* { box-sizing: border-box; }
body { font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif;
  color:var(--ink); background:var(--bg); margin:0; line-height:1.75; }
.page { max-width:880px; margin:0 auto; padding:48px 40px 96px;
  background:#fff; min-height:100vh; box-shadow:0 0 24px rgba(31,41,51,.06); }
h1 { font-size:1.9em; border-bottom:3px solid var(--accent); padding-bottom:.3em; }
h2 { font-size:1.35em; margin-top:2em; border-left:5px solid var(--accent); padding-left:.5em; }
h3 { font-size:1.1em; margin-top:1.6em; }
table { border-collapse:collapse; width:100%; margin:1em 0; font-size:.92em; }
th { background:var(--accent); color:#fff; }
th,td { border:1px solid var(--line); padding:8px 10px; text-align:left; }
tr:nth-child(even) td { background:var(--bg); }
code { background:#eef2f3; padding:2px 5px; border-radius:4px; font-size:.9em; }
pre { background:#1f2933; color:#e6edf3; padding:14px; border-radius:8px; overflow-x:auto; }
pre code { background:none; color:inherit; }
blockquote { border-left:4px solid var(--accent); background:var(--bg);
  margin:1em 0; padding:.6em 1em; color:#52606d; }
img { max-width:100%; }
a { color:var(--accent); }
.watermark { text-align:right; color:#9aa5b1; font-size:.85em; margin-top:64px;
  border-top:1px solid var(--line); padding-top:12px; }
@media print { body{background:#fff} .page{box-shadow:none; padding:0} }
"""


def convert(src_md: Path, dst_html: Path) -> None:
    md_text = src_md.read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{src_md.stem}</title>
<style>{CSS}</style>
</head>
<body><div class="page">
{body}
<div class="watermark">© MiaoYu · 生成自 {src_md.name}</div>
</div></body>
</html>
"""
    dst_html.write_text(html, encoding="utf-8")
    print(f"OK: {dst_html} ({len(html)//1024} KB)")


if __name__ == "__main__":
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
