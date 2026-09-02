# -*- coding: utf-8 -*-
"""主对话宪法契约：派发规则、检查点三类、双通道矩阵、复核纪律必须在场。"""
from pathlib import Path

CLAUDE_MD = Path(__file__).resolve().parent.parent / "CLAUDE.md"

REQUIRED = [
    # 5 个从对话名全部被引用（派发对象）
    "qa-archaeologist", "qa-case-positive", "qa-case-negative",
    "qa-executor", "qa-reporter",
    # 检查点三类
    "BUG 定级争议", "测试范围取舍", "不可逆动作",
    # 双通道对抗的合并与复核规则
    "合并去重", "复核",
    # 运行逻辑：产物落盘
    "摘要和产物路径",
    # 证据纪律
    "没有证据=没完成",
]


def test_orchestrator_constitution():
    assert CLAUDE_MD.is_file(), "CLAUDE.md 缺失"
    text = CLAUDE_MD.read_text(encoding="utf-8")
    for kw in REQUIRED:
        assert kw in text, f"宪法缺少关键规则: {kw}"
