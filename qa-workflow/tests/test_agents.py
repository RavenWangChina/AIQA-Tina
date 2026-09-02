# -*- coding: utf-8 -*-
"""从对话定义契约：frontmatter 完整 + 共用运行逻辑原文在场 + 职能边界。"""
import re
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "agents"

AGENT_FILES = {
    "qa-archaeologist.md": ["模块卡片", "接口清单", "01-系统认知"],
    "qa-case-positive.md": ["正向", "做了该做的", "02-用例库"],
    "qa-case-negative.md": ["破坏者", "逆向", "模式库"],
    "qa-executor.md": ["checklist", "证据", "Allure"],
    "qa-reporter.md": ["BUG 报告", "禅道", "周期汇报"],
}

# 共用运行逻辑（spec 第 2 节）：每个 agent 定义必须原文包含这四条的完整表述
COMMON_RUNTIME = [
    "开工先读知识库 00-索引.md",
    "只干职能内的事",
    "完整产物写入知识库文件，只回传摘要和产物路径",
    "从对话之间不通信",
]


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "缺少 frontmatter"
    kv = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            kv[k.strip()] = v.strip()
    return kv


def test_agents_frontmatter_and_common_runtime():
    for fname, duty_keys in AGENT_FILES.items():
        path = AGENTS_DIR / fname
        assert path.is_file(), f"agent 定义缺失: {fname}"
        text = path.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        assert fm.get("name"), f"{fname} frontmatter 缺 name"
        assert "description" in fm, f"{fname} frontmatter 缺 description"
        for kw in COMMON_RUNTIME:
            assert kw in text, f"{fname} 缺共用运行逻辑: {kw}"
        for kw in duty_keys:
            assert kw in text, f"{fname} 缺职能关键词: {kw}"
