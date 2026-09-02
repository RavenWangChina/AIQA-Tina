# -*- coding: utf-8 -*-
"""知识库模板内容契约：每个模板必须含其职责内的关键 section/字段。"""
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
KBASE = PKG / "qa-knowledge"

# 模板路径 -> 必须包含的文本片段（spec 第 3/6/7 节定义的字段）
REQUIRED_SECTIONS = {
    "00-索引.md": ["模块清单", "各库状态"],
    "01-系统认知/模块卡片模板.md": ["入口", "依赖", "接口清单", "数据流", "已知坑"],
    "01-系统认知/接口清单模板.md": ["路径", "参数", "鉴权", "归属模块"],
    "02-用例库/L2功能模板.md": ["前置", "步骤", "预期", "TC-"],
    "02-用例库/L3场景模板.md": ["场景", "步骤", "预期"],
    "02-用例库/L4探索模板.md": ["探索", "观察", "疑点"],
    "03-BUG库/模式库模板.md": ["特征", "高发模块", "反哺"],
    "03-BUG库/报告模板.md": [
        "定级", "复现概率", "环境", "使用的测试方法", "复现步骤",
        "预期 vs 实际", "证据链", "归因初判", "禅道",
    ],
    "04-报告库/轮次模板.md": ["范围", "用例执行结果", "BUG 清单", "证据链索引"],
    "04-报告库/周期汇报模板.md": [
        "本周范围", "进度", "质量态势", "趋势", "风险与求助",
    ],
}


def test_every_template_has_required_sections():
    for rel, keys in REQUIRED_SECTIONS.items():
        path = KBASE / rel
        assert path.is_file(), f"模板缺失: {rel}"
        text = path.read_text(encoding="utf-8")
        for kw in keys:
            assert kw in text, f"{rel} 缺少字段: {kw}"
