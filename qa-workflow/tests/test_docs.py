# -*- coding: utf-8 -*-
"""渲染契约：HTML 自包含（无外链）、含文档关键内容、含作者水印。"""
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
HTML = PKG / "docs" / "2026-09-02-qa-test-workflow-design.html"
MAKE = PKG / "docs" / "make_doc_html.py"
DEPLOY = PKG / "docs" / "部署手册.md"


def test_make_doc_html_script_exists():
    assert MAKE.is_file()


def test_html_selfcontained_and_has_content():
    text = HTML.read_text(encoding="utf-8")
    assert "<html" in text
    # 自包含：不允许外部样式/脚本引用（src=/href= 指向 http）
    import re
    ext = re.findall(r'(?:src|href)="http[^"]*"', text)
    assert not ext, f"发现外链，破坏自包含: {ext[:3]}"
    # 关键内容与水印
    for kw in ["双环", "一主多从", "双通道", "Raven Wang", "实施路线"]:
        assert kw in text, f"HTML 缺关键内容: {kw}"


def test_deploy_guide_sections():
    text = DEPLOY.read_text(encoding="utf-8")
    for kw in ["selfcheck", "install-batch1", "CLAUDE.md", "禅道", "iOS"]:
        assert kw in text, f"部署手册缺: {kw}"
