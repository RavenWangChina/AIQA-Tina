# QA 测试工作流包

双环（测试环+知识环）× 一主多从架构的 QA 工作流，完整设计见
`docs/superpowers/specs/2026-09-02-qa-test-workflow-design.md`（本包 docs/ 内有其静态网页版）。

## 目录

- `CLAUDE.md` —— 主对话编排宪法（部署时复制到工作目录根）
- `.claude/agents/` —— 5 个从对话定义（考古/正向用例/逆向用例/执行/报告）
- `qa-knowledge/` —— 知识库骨架与全部模板
- `scripts/selfcheck.py` —— 结构自检
- `tools/install-batch1.ps1` —— 第一批工具安装
- `tests/` —— 包结构契约测试

## 部署

见 `docs/部署手册.md`。

© MiaoYu · 2026年09月02日
