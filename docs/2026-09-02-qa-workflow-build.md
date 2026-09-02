# QA 测试工作流体系搭建 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已批准的 QA 工作流设计（双环 × 一主多从）落成一个可部署、可自检的工作流包 `qa-workflow/`。

**Architecture:** 纯文件体系——知识库模板 + 5 个从对话 agent 定义 + 主对话编排宪法（CLAUDE.md）+ pytest 结构自检 + 工具安装脚本 + 单文件静态网页版设计文档。零后端服务。

**Tech Stack:** Markdown、Claude Code agents（frontmatter 格式）、Python 3.10+（pytest 做结构校验、markdown 库渲染 HTML）、PowerShell（工具安装脚本）。

**Spec:** `docs/superpowers/specs/2026-09-02-qa-test-workflow-design.md`（执行者须同时读 spec）

## Global Constraints

- 包根目录：`qa-workflow/`（在开发仓库的隔离 worktree 内搭建，交付时可整体拷走）
- 所有模板文件必须包含 spec 第 3/6/7 节定义的字段，不得自创字段名
- agent 定义使用 Claude Code agents frontmatter 格式（name/description/tools/model）
- 从对话共用运行逻辑（读 00-索引 → 只干职能内 → 产物落盘回传指针 → 向主对话汇报）必须原文出现在每个 agent 定义中
- 测试命令统一：`python -m pytest qa-workflow/tests/ -v`（Windows，Git Bash）
- 中文注释、中文文档；工具名/命令/路径保留英文原文
- 每个任务的产出必须通过对应测试才算完成（证据先于结论）

---

### Task 1: 包骨架与结构校验测试

**Files:**
- Create: `qa-workflow/README.md`
- Create: `qa-workflow/tests/__init__.py`（空文件）
- Create: `qa-workflow/tests/test_structure.py`

**Interfaces:**
- Consumes: 无（首任务）
- Produces: 目录树契约（后续任务按此创建文件）：

```
qa-workflow/
├── README.md
├── CLAUDE.md                                  ← Task 4
├── .claude/agents/qa-archaeologist.md          ← Task 3
├── .claude/agents/qa-case-positive.md          ← Task 3
├── .claude/agents/qa-case-negative.md          ← Task 3
├── .claude/agents/qa-executor.md               ← Task 3
├── .claude/agents/qa-reporter.md               ← Task 3
├── qa-knowledge/00-索引.md                     ← Task 2
├── qa-knowledge/01-系统认知/模块卡片模板.md      ← Task 2
├── qa-knowledge/01-系统认知/接口清单模板.md      ← Task 2
├── qa-knowledge/02-用例库/L1冒烟模板.yaml        ← Task 2
├── qa-knowledge/02-用例库/L2功能模板.md          ← Task 2
├── qa-knowledge/02-用例库/L3场景模板.md          ← Task 2
├── qa-knowledge/02-用例库/L4探索模板.md          ← Task 2
├── qa-knowledge/03-BUG库/模式库模板.md           ← Task 2
├── qa-knowledge/03-BUG库/报告模板.md             ← Task 2
├── qa-knowledge/04-报告库/轮次模板.md            ← Task 2
├── qa-knowledge/04-报告库/周期汇报模板.md         ← Task 2
├── scripts/selfcheck.py                        ← Task 5
├── tools/install-batch1.ps1                    ← Task 5
├── tests/                                     ← Task 1
└── docs/2026-09-02-qa-test-workflow-design.html ← Task 6
```

- [ ] **Step 1: 写失败的结构测试**

创建 `qa-workflow/tests/test_structure.py`：

```python
# -*- coding: utf-8 -*-
"""qa-workflow 包结构契约测试：目录树必须与 Task 1 Interfaces 定义完全一致。"""
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent

EXPECTED_FILES = [
    "README.md",
    "CLAUDE.md",
    ".claude/agents/qa-archaeologist.md",
    ".claude/agents/qa-case-positive.md",
    ".claude/agents/qa-case-negative.md",
    ".claude/agents/qa-executor.md",
    ".claude/agents/qa-reporter.md",
    "qa-knowledge/00-索引.md",
    "qa-knowledge/01-系统认知/模块卡片模板.md",
    "qa-knowledge/01-系统认知/接口清单模板.md",
    "qa-knowledge/02-用例库/L1冒烟模板.yaml",
    "qa-knowledge/02-用例库/L2功能模板.md",
    "qa-knowledge/02-用例库/L3场景模板.md",
    "qa-knowledge/02-用例库/L4探索模板.md",
    "qa-knowledge/03-BUG库/模式库模板.md",
    "qa-knowledge/03-BUG库/报告模板.md",
    "qa-knowledge/04-报告库/轮次模板.md",
    "qa-knowledge/04-报告库/周期汇报模板.md",
    "scripts/selfcheck.py",
    "tools/install-batch1.ps1",
    "docs/2026-09-02-qa-test-workflow-design.html",
]


def test_all_expected_files_exist():
    missing = [f for f in EXPECTED_FILES if not (PKG / f).is_file()]
    assert not missing, f"缺少文件: {missing}"


def test_no_stray_top_level_entries():
    allowed = {
        "README.md", "CLAUDE.md", ".claude", "qa-knowledge",
        "scripts", "tools", "tests", "docs",
    }
    actual = {p.name for p in PKG.iterdir()}
    stray = actual - allowed
    assert not stray, f"包根目录出现多余条目: {stray}"
```

同时创建空的 `qa-workflow/tests/__init__.py`。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest qa-workflow/tests/test_structure.py -v`
Expected: FAIL（`test_all_expected_files_exist` 报缺少大量文件）

- [ ] **Step 3: 创建 README.md 与全部目录**

创建 `qa-workflow/README.md`：

```markdown
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

见 `docs/部署手册.md`（搭好后生成）。

© Raven Wang · 2026年09月02日
```

创建空目录：`qa-knowledge/01-系统认知`、`qa-knowledge/02-用例库`、`qa-knowledge/03-BUG库`、`qa-knowledge/04-报告库`、`docs/`（空目录用占位方式：后续任务立即填文件，无需 .gitkeep）。

- [ ] **Step 4: 运行测试，确认仍失败但只剩文件缺失**

Run: `python -m pytest qa-workflow/tests/test_structure.py -v`
Expected: `test_no_stray_top_level_entries` PASS（目录齐了且无多余项——注意 git 不跟踪空目录，跑测试时以文件系统现状为准）；`test_all_expected_files_exist` 仍 FAIL（文件由后续任务补齐）

- [ ] **Step 5: Commit**

```bash
git add qa-workflow/
git commit -m "qa-workflow: 包骨架与结构契约测试"
```

---

### Task 2: 知识库模板全套（内容来自 spec 第 3/6/7 节）

**Files:**
- Create: `qa-knowledge/00-索引.md` 及 Task 1 Interfaces 列出的 11 个模板文件
- Create: `qa-workflow/tests/test_templates.py`

**Interfaces:**
- Consumes: Task 1 的目录树
- Produces: 11 个模板文件路径（后续 agent 定义与自检脚本按名引用）；模板关键字段清单（test_templates.py 中的 `REQUIRED_SECTIONS` 字典——Task 5 的 selfcheck.py 复用同一契约）

- [ ] **Step 1: 写失败的模板字段测试**

创建 `qa-workflow/tests/test_templates.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest qa-workflow/tests/test_templates.py -v`
Expected: FAIL（模板缺失）

- [ ] **Step 3: 创建全部 11 个模板文件**

`qa-knowledge/00-索引.md`：

```markdown
# 00-索引（主对话工作记忆，每次开工先读本文件）

> 维护规则：任何库有新增/状态变化，对应行的"最后更新"必须改。本文件是主对话的入口地图。

## 模块清单

| 模块 | 卡片路径 | 用例状态 | 最近测试轮次 |
|------|----------|----------|--------------|
| （示例）登录 | 01-系统认知/模块卡片/登录.md | L1-L2 已建 | 04-报告库/轮次/2026-09-02-登录/ |

## 各库状态

- 01-系统认知：已建卡片 N 张 / 覆盖模块 M 个（目标：全部）
- 02-用例库：L1 冒烟 N 条 | L2 功能 N 条 | L3 场景 N 条 | L4 探索 N 条；自动化率 X%
- 03-BUG库：累计 N 个（L1 致命 x / L2 主要 x / L3 次要 x / L4 轻微 x）；模式库 N 条
- 04-报告库：轮次 N 份 | 汇总 N 份
```

`qa-knowledge/01-系统认知/模块卡片模板.md`：

```markdown
# 模块卡片：<模块名>

> 考古从产出。每个功能模块一张；信息有变必须更新本卡片而不是另开新文件。

## 入口
（页面路由 / Activity/ViewController / API 调用链的起点）

## 依赖
（上游模块、下游服务、第三方 SDK、硬件依赖）

## 接口清单
（本模块调用的服务端 API，引用 01-系统认知/接口清单.md 的行号或锚点）

## 数据流
（数据从哪来、经过什么转换、存到哪、谁读它）

## 已知坑
（考古发现的历史问题、特殊逻辑、魔法值——逆向用例从的重点关注区）
```

`qa-knowledge/01-系统认知/接口清单模板.md`：

```markdown
# 接口清单（契约基线）

> 考古从产出并维护。本文件同时是契约测试的基线（spec 第 4 节 #6）。

| API | 路径 | 方法 | 参数 | 鉴权 | 归属模块 | 备注 |
|-----|------|------|------|------|----------|------|
| （示例）登录 | /api/auth/login | POST | username,password | 无 | 登录 | |
```

`qa-knowledge/02-用例库/L1冒烟模板.yaml`：

```yaml
# L1 冒烟用例（可自动化，Maestro YAML 原生格式）
# 主路径可用性验证：跑不过=版本不可测，立即阻塞
appId: com.example.app            # 部署时替换为实际包名
name: 冒烟-<模块名>-主路径
tags:
  - L1
  - <模块名>
---
- launchApp
- assertVisible: ".*<主页面关键元素>.*"
```

`qa-knowledge/02-用例库/L2功能模板.md`：

```markdown
# L2 功能用例 · <模块名>

> 正向用例从与逆向用例从分文件产出（正向存 `L2功能-正向.md`，逆向存 `L2功能-逆向.md`），主对话合并。

## TC-<模块缩写>-001 <用例标题>

- 前置：（账号状态/设备状态/网络状态）
- 级别：L2
- 来源：正向 | 逆向
- 步骤：
  1. …
  2. …
- 预期：…
- 自动化：可自动化（工具：maestro|pytest）| 仅手工
```

`qa-knowledge/02-用例库/L3场景模板.md`：

```markdown
# L3 场景用例 · <模块名>

> 端到端组合场景：跨模块、跨端（App↔服务端↔音箱）、含环境切换。

## SC-<编号> <场景标题>

- 场景：（谁在什么环境下完成什么跨模块流程）
- 步骤：
  1. …
- 预期：…
- 涉及模块：
```

`qa-knowledge/02-用例库/L4探索模板.md`：

```markdown
# L4 探索性测试笔记 · <模块名>

> 探索不是乱点：带着假设去探索，观察记录下来喂回知识库。

## EX-<编号> <探索主题>

- 假设：（我怀疑……在……条件下会……）
- 操作路径：（实际点了什么）
- 观察：（实际发生了什么）
- 疑点：（值得跟进的异常 → 升级为 BUG 报告或逆向用例）
```

`qa-knowledge/03-BUG库/模式库模板.md`：

```markdown
# BUG 模式库

> 每个 bug 归档时同步更新。反哺规则：同特征 bug 第二次出现，逆向用例从必须加针对性用例（spec 第 6 节硬规则 4）。

| 模式编号 | 特征 | 高发模块 | 出现次数 | 反哺动作 | 相关 BUG |
|----------|------|----------|----------|----------|----------|
| P-001 | （如：列表不自动刷新类） | 配网 | 2 | 逆向用例从加"状态变更后 UI 刷新"检查项 | BUG-…-001, BUG-…-014 |
```

`qa-knowledge/03-BUG库/报告模板.md`：

```markdown
# BUG-<YYYY-MM-DD>-<编号> 【<模块名>】<一句话标题>

## 定级
严重级：L1致命 | L2主要 | L3次要 | L4轻微（四选一）
优先级：高 | 中 | 低
复现概率：N/M（真实计数，禁写"偶现"）

## 环境（自动采集，禁手填）
- 服务端版本：{commit/版本号}　测试环境：{域名/IP}
- Android：{机型/系统/App 版本}　iOS：{机型/系统/App 版本}
- 音箱固件：{版本}　网络：{WiFi 2.4G/5G/弱网}

## 使用的测试方法
{测试类型（spec 第 4 节矩阵 #）} | 用例：02-用例库/<模块>/…#TC-xx

## 复现步骤
1. …（可执行、无歧义）

## 预期 vs 实际
- 预期：…
- 实际：…

## 证据链（同目录归档）
- 截图/ 或 录屏.mp4（adb screenrecord / iOS 系统录屏）
- logcat 片段.txt（时间戳 + 关键行标红）
- 抓包.har（如涉及网络）

## 归因初判（非定论）
（考古从/执行从给出，指向疑似模块）

## 禅道
bug 单号：（提交后回填）
```

`qa-knowledge/04-报告库/轮次模板.md`：

```markdown
# 测试轮次报告 · <日期>-<模块名>

## 范围
（本轮测什么：禅道单号/指令来源、模块、测试级别 L1-L4 到哪层、双通道矩阵覆盖了哪几行）

## 用例执行结果
| 用例 | 结果 | 证据 |
|------|------|------|
| TC-xx-001 | PASS/FAIL/BLOCKED | 附件路径或截图 |

## BUG 清单
（本轮新增 BUG 索引，链接 03-BUG库/归档/…）

## 证据链索引
（Allure 报告路径 + 关键截图/日志清单）
```

`qa-knowledge/04-报告库/周期汇报模板.md`：

```markdown
# <周期>测试汇报（呈领导）

## 一、本周范围
（禅道单 + 指令；测了哪些模块）

## 二、进度
知识库覆盖 X/Y 模块；用例 L1 冒烟 N 条 / L2 功能 N 条 / L3 场景 N 条 / L4 探索 N 条；自动化率 X%

## 三、质量态势
新增 bug N（L1 x / L2 x / L3 x / L4 x）；修复回归 M；遗留风险 TOP3

## 四、趋势
覆盖率/bug 收敛（周环比，数据来自报告库轮次记录）

## 五、风险与求助
（如：iOS WDA 证书维护、弱网环境不足）
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest qa-workflow/tests/test_templates.py -v`
Expected: PASS（10 个模板字段齐全）

- [ ] **Step 5: Commit**

```bash
git add qa-workflow/qa-knowledge/ qa-workflow/tests/test_templates.py
git commit -m "qa-workflow: 知识库模板全套（spec 3/6/7 节落地）"
```

---

### Task 3: 五个从对话 agent 定义

**Files:**
- Create: `qa-workflow/.claude/agents/qa-archaeologist.md`
- Create: `qa-workflow/.claude/agents/qa-case-positive.md`
- Create: `qa-workflow/.claude/agents/qa-case-negative.md`
- Create: `qa-workflow/.claude/agents/qa-executor.md`
- Create: `qa-workflow/.claude/agents/qa-reporter.md`
- Create: `qa-workflow/tests/test_agents.py`

**Interfaces:**
- Consumes: Task 2 的模板路径（agent 定义中按名引用）
- Produces: 5 个 agent 名（`qa-archaeologist` 等，主对话 CLAUDE.md 按 name 派发）；共用运行逻辑常量文本 `COMMON_RUNTIME`（test_agents.py 中定义，Task 5 selfcheck 复用）

- [ ] **Step 1: 写失败的 agent 定义测试**

创建 `qa-workflow/tests/test_agents.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest qa-workflow/tests/test_agents.py -v`
Expected: FAIL（文件缺失）

- [ ] **Step 3: 创建 5 个 agent 定义**

每个文件结构相同，以下给出全部五个。共用运行逻辑段四条原文相同（test 断言依赖）。

`qa-workflow/.claude/agents/qa-archaeologist.md`：

```markdown
---
name: qa-archaeologist
description: 考古从：对指定模块做源码逆向，产出模块卡片与接口清单，写入知识库 01-系统认知
tools: Read, Grep, Glob, Bash, Agent
model: sonnet
---

# 考古从（qa-archaeologist）

## 共用运行逻辑（不可省略、不可改写）

1. 开工先读知识库 00-索引.md。
2. 只干职能内的事。
3. 完整产物写入知识库文件，只回传摘要和产物路径。
4. 从对话之间不通信。

## 职能

对主对话指定的模块范围做源码逆向：

- 按 `qa-knowledge/01-系统认知/模块卡片模板.md` 产出模块卡片（入口/依赖/接口清单/数据流/已知坑），写入 `01-系统认知/模块卡片/<模块名>.md`
- 本模块涉及的服务端 API 按 `接口清单模板.md` 补进 `01-系统认知/接口清单.md`（增量追加，不覆盖他人行）
- "已知坑"一节是逆向用例从的粮草：历史 hack、魔法值、特殊分支必须记录

## 边界

- 不设计用例、不执行测试、不写 BUG 报告（其他从对话职责）
- 源码读不懂的地方标注「待确认」留给主对话，不猜测填充
- 完成后更新 00-索引.md 模块清单行，回传：产物文件路径 + 一句话摘要
```

`qa-workflow/.claude/agents/qa-case-positive.md`：

```markdown
---
name: qa-case-positive
description: 正向用例从：验证功能做了该做的，按 L1-L4 分级产出正向用例，写入知识库 02-用例库
tools: Read, Grep, Glob, Write, Edit
model: sonnet
---

# 正向用例从（qa-case-positive）

## 共用运行逻辑（不可省略、不可改写）

1. 开工先读知识库 00-索引.md。
2. 只干职能内的事。
3. 完整产物写入知识库文件，只回传摘要和产物路径。
4. 从对话之间不通信。

## 职能（通道 A：功能做了该做的）

- 输入：主对话给的模块名 + 测试级别（L1-L4）
- 读该模块的模块卡片（01-系统认知/模块卡片/<模块名>.md），从"入口/数据流"推主路径与分支路径
- 按 `02-用例库/` 对应级别模板产出正向用例，存 `02-用例库/<模块名>/L2功能-正向.md`（或 L1/L3/L4 对应文件）
- 可自动化的用例直接写工具原生格式（Maestro YAML / pytest），用例即脚本

## 边界

- 立场是"验证该做的做了"——不设计破坏性输入（那是逆向用例从的职责，两个立场是对抗设计）
- 不读逆向用例从的文件，不合并（合并是主对话职责）
- 完成后回传：用例文件路径 + 用例条数 + 覆盖的功能点清单
```

`qa-workflow/.claude/agents/qa-case-negative.md`：

```markdown
---
name: qa-case-negative
description: 逆向用例从：破坏者立场设计用例（边界/非法输入/并发/中断/断网），写入知识库 02-用例库
tools: Read, Grep, Glob, Write, Edit
model: sonnet
---

# 逆向用例从（qa-case-negative）

## 共用运行逻辑（不可省略、不可改写）

1. 开工先读知识库 00-索引.md。
2. 只干职能内的事。
3. 完整产物写入知识库文件，只回传摘要和产物路径。
4. 从对话之间不通信。

## 职能（通道 B：破坏者立场）

- 输入：主对话给的模块名 + 测试级别
- 读模块卡片的"已知坑"一节 + `03-BUG库/模式库.md` 全文——历史坑和 bug 模式是破坏用例的第一来源
- 破坏维度清单（每轮至少过一遍）：边界值、非法/超长/空输入、并发冲突、操作中途取消、断网重试、权限缺失、状态跳跃
- 产出存 `02-用例库/<模块名>/L2功能-逆向.md`（或对应级别文件），格式与正向一致（TC- 编号、来源标"逆向"）

## 反哺规则

模式库中该模块相关模式每出现一次，本轮必须新增至少一条针对性破坏用例。

## 边界

- 不读正向用例从的文件；不执行测试
- 完成后回传：用例文件路径 + 条数 + 覆盖的破坏维度
```

`qa-workflow/.claude/agents/qa-executor.md`：

```markdown
---
name: qa-executor
description: 执行从：执行自动化用例（pytest/Maestro/adb/go-ios/k6/ZAP 等）并编排人工真机环节，产出执行记录与证据
tools: Read, Bash, Write, Glob, Grep
model: sonnet
---

# 执行从（qa-executor）

## 共用运行逻辑（不可省略、不可改写）

1. 开工先读知识库 00-索引.md。
2. 只干职能内的事。
3. 完整产物写入知识库文件，只回传摘要和产物路径。
4. 从对话之间不通信。

## 职能

- 输入：主对话给的用例清单 + 环境信息（服务端地址/设备/账号）
- 自动化执行：pytest+httpx（API）、Maestro（Android UI）、adb / go-ios+WDA（底层操作与证据采集）、k6（性能）、ZAP/nuclei（安全）、Schemathesis（契约+Fuzz）、Fastbot（稳定性）、Toxiproxy（弱网）
- 双通道验证（spec 第 4 节矩阵）：程序断言之外，截图交给视觉断言通道；断言过但画面错仍算 BUG
- 人工环节编排：音响实体操作等智能体碰不了的部分，生成「操作 checklist + 记录模板」交主对话转人工，人做完回填，证据照常归档
- 环境**自动采集**（adb/服务端 API 取版本），禁手填
- 证据落 `04-报告库/轮次/<日期>-<模块>/`（截图/录屏/logcat 片段/抓包），pytest 侧开 `--alluredir` 让结果进 Allure

## 边界

- 不定级、不写 BUG 报告正文（只采集证据上报）；不直接向禅道提单
- 完成后回传：执行记录路径 + 通过/失败/BLOCKED 计数 + 证据目录路径
```

`qa-workflow/.claude/agents/qa-reporter.md`：

```markdown
---
name: qa-reporter
description: 报告从：汇总轮次产物生成 BUG 报告与周期汇报（复核通过前不外发）
tools: Read, Glob, Write, Grep
model: sonnet
---

# 报告从（qa-reporter）

## 共用运行逻辑（不可省略、不可改写）

1. 开工先读知识库 00-索引.md。
2. 只干职能内的事。
3. 完整产物写入知识库文件，只回传摘要和产物路径。
4. 从对话之间不通信。

## 职能

- BUG 报告：按 `03-BUG库/报告模板.md` 生成，证据从执行从的轮次目录引用（不复制，写相对路径）；复现概率用执行记录的真实计数
- 轮次报告：按 `04-报告库/轮次模板.md` 汇总本轮用例结果与证据链索引
- 周期汇报：按 `04-报告库/周期汇报模板.md` 从 00-索引与报告库自动汇总数据，不手写数字

## 边界（双通道复核纪律）

- 生成的 BUG 报告**不直接入禅道**——交主对话复核（步骤可复现？证据齐？定级准？），复核过了才经禅道 MCP 提单
- 复现概率禁写"偶现"；环境字段引用执行从的自动采集结果
- 完成后回传：报告路径清单 + 每份报告的一句话摘要
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest qa-workflow/tests/test_agents.py -v`
Expected: PASS（5 个定义 frontmatter/共用逻辑/职能词齐全）

- [ ] **Step 5: Commit**

```bash
git add qa-workflow/.claude/ qa-workflow/tests/test_agents.py
git commit -m "qa-workflow: 五个从对话 agent 定义（含共用运行逻辑与对抗立场边界）"
```

---

### Task 4: 主对话编排宪法 CLAUDE.md

**Files:**
- Create: `qa-workflow/CLAUDE.md`
- Create: `qa-workflow/tests/test_orchestrator.py`

**Interfaces:**
- Consumes: Task 3 的 5 个 agent name；Task 2 的知识库路径
- Produces: `qa-workflow/CLAUDE.md`（部署时复制到目标工作目录根，Claude Code 自动加载）

- [ ] **Step 1: 写失败的宪法契约测试**

创建 `qa-workflow/tests/test_orchestrator.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest qa-workflow/tests/test_orchestrator.py -v`
Expected: FAIL（CLAUDE.md 缺失）

- [ ] **Step 3: 写 CLAUDE.md**

创建 `qa-workflow/CLAUDE.md`：

```markdown
# QA 测试工作流 · 主对话编排宪法

> 部署方式：本文件复制到 QA 工作目录根（含 qa-knowledge/ 的目录），Claude Code 自动加载。
> 从对话定义在 `.claude/agents/`（五个）。完整设计：docs/superpowers/specs/2026-09-02-qa-test-workflow-design.md

## 你是主对话（编排者）

唯一入口。接禅道工单（zentao MCP）或人工指令 → 拆解任务 → 派发从对话 → 汇总归纳 → 产出报告。
你不亲自读源码考古、不亲自写用例、不亲自跑测试——这些是从对话的职责。你的价值在拆解、派发、合并、裁决。

## 每轮测试的标准编排

1. 读 `qa-knowledge/00-索引.md`（工作记忆）
2. 若目标模块无模块卡片 → 先派 `qa-archaeologist` 考古
3. 派用例双从（**并行、互不可见**）：`qa-case-positive` + `qa-case-negative`，各自按模板产出
4. 收两份用例后**合并去重**——覆盖缺口（两从都没碰的功能点或破坏维度）即分歧点，停下来报用户
5. 派 `qa-executor` 执行（声明本轮测试级别 L1-L4 与覆盖的双通道矩阵行）
6. 派 `qa-reporter` 生成 BUG 报告与轮次报告
7. 你复核 BUG 报告（步骤可复现？证据齐？定级准？）——复核过了才经禅道 MCP 提单
8. 提示知识库回写（模式库、00-索引状态行）

## 检查点规则（只在三类节点停下来问用户）

- **BUG 定级争议**：执行从/报告从/你三方定级不一致时
- **测试范围取舍**：时间不够砍哪层（L4→L3 顺序砍）、砍哪个模块
- **不可逆动作**：向禅道提单（对外可见）、删除/覆盖知识库既有内容

其余自主推进。

## 证据纪律

**没有证据=没完成。** 执行从没给截图/日志/Allure 产物的轮次，不接受其"通过"结论；BUG 报告没证据链不提单。

## 从对话管理

- 从对话产物全部落知识库文件，回传摘要和产物路径（摘要瓶颈对策）
- 从对话失败可重派（知识库即断点）；同任务重派最多 2 次后停下来报用户
- token 路由：考古/用例类用 sonnet，纯执行类工具调用不限制
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest qa-workflow/tests/test_orchestrator.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add qa-workflow/CLAUDE.md qa-workflow/tests/test_orchestrator.py
git commit -m "qa-workflow: 主对话编排宪法"
```

---

### Task 5: 自检脚本 + 第一批工具安装脚本

**Files:**
- Create: `qa-workflow/scripts/selfcheck.py`
- Create: `qa-workflow/tools/install-batch1.ps1`
- Create: `qa-workflow/tests/test_selfcheck.py`

**Interfaces:**
- Consumes: Task 1-4 的全部契约（结构/模板/agent/宪法）
- Produces: `selfcheck.py`（目标机器部署后跑一次即知包是否完整；exit code 0=完整）；`install-batch1.ps1`（Windows 工具安装）

- [ ] **Step 1: 写失败的 selfcheck 测试**

创建 `qa-workflow/tests/test_selfcheck.py`：

```python
# -*- coding: utf-8 -*-
"""selfcheck.py 契约：复用 tests 里的四类契约，入口可执行，报告格式固定。"""
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPT = PKG / "scripts" / "selfcheck.py"


def test_selfcheck_runs_and_passes_on_intact_package():
    # 包已由 Task1-4 建好，selfcheck 应全绿退出 0
    r = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", cwd=str(PKG),
    )
    assert r.returncode == 0, f"selfcheck 失败:\n{r.stdout}\n{r.stderr}"
    for section in ["结构", "模板", "从对话", "宪法"]:
        assert section in r.stdout, f"报告缺板块: {section}"
    assert "全部通过" in r.stdout


def test_selfcheck_detects_missing_file(tmp_path):
    # 破坏一个文件（拷贝包到临时目录删除一个），selfcheck 必须非 0 退出
    import shutil
    broken = tmp_path / "broken"
    shutil.copytree(PKG, broken, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    victim = broken / "qa-knowledge" / "00-索引.md"
    victim.unlink()
    r = subprocess.run(
        [sys.executable, str(broken / "scripts" / "selfcheck.py")],
        capture_output=True, text=True, encoding="utf-8", cwd=str(broken),
    )
    assert r.returncode != 0, "包损坏时 selfcheck 竟然通过了"
    assert "00-索引.md" in r.stdout
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest qa-workflow/tests/test_selfcheck.py -v`
Expected: FAIL（selfcheck.py 不存在）

- [ ] **Step 3: 实现 selfcheck.py**

创建 `qa-workflow/scripts/selfcheck.py`（把四类契约内联为独立脚本，不 import tests，目标机器没有 pytest 也要能跑）：

```python
# -*- coding: utf-8 -*-
"""qa-workflow 包自检：结构 / 模板 / 从对话 / 宪法 四类契约。
用法：python scripts/selfcheck.py（在包根执行）
退出码：0=全部通过；1=有缺失（stdout 列出明细）。目标机器部署后先跑本脚本。"""
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent

EXPECTED_FILES = [
    "README.md", "CLAUDE.md",
    ".claude/agents/qa-archaeologist.md", ".claude/agents/qa-case-positive.md",
    ".claude/agents/qa-case-negative.md", ".claude/agents/qa-executor.md",
    ".claude/agents/qa-reporter.md",
    "qa-knowledge/00-索引.md",
    "qa-knowledge/01-系统认知/模块卡片模板.md", "qa-knowledge/01-系统认知/接口清单模板.md",
    "qa-knowledge/02-用例库/L1冒烟模板.yaml", "qa-knowledge/02-用例库/L2功能模板.md",
    "qa-knowledge/02-用例库/L3场景模板.md", "qa-knowledge/02-用例库/L4探索模板.md",
    "qa-knowledge/03-BUG库/模式库模板.md", "qa-knowledge/03-BUG库/报告模板.md",
    "qa-knowledge/04-报告库/轮次模板.md", "qa-knowledge/04-报告库/周期汇报模板.md",
    "tools/install-batch1.ps1",
    "docs/2026-09-02-qa-test-workflow-design.html",
    "docs/部署手册.md",
]

REQUIRED_SECTIONS = {
    "qa-knowledge/00-索引.md": ["模块清单", "各库状态"],
    "qa-knowledge/01-系统认知/模块卡片模板.md": ["入口", "依赖", "接口清单", "数据流", "已知坑"],
    "qa-knowledge/01-系统认知/接口清单模板.md": ["路径", "参数", "鉴权", "归属模块"],
    "qa-knowledge/02-用例库/L2功能模板.md": ["前置", "步骤", "预期", "TC-"],
    "qa-knowledge/02-用例库/L3场景模板.md": ["场景", "步骤", "预期"],
    "qa-knowledge/02-用例库/L4探索模板.md": ["探索", "观察", "疑点"],
    "qa-knowledge/03-BUG库/模式库模板.md": ["特征", "高发模块", "反哺"],
    "qa-knowledge/03-BUG库/报告模板.md": ["定级", "复现概率", "环境", "使用的测试方法", "复现步骤", "预期 vs 实际", "证据链", "归因初判", "禅道"],
    "qa-knowledge/04-报告库/轮次模板.md": ["范围", "用例执行结果", "BUG 清单", "证据链索引"],
    "qa-knowledge/04-报告库/周期汇报模板.md": ["本周范围", "进度", "质量态势", "趋势", "风险与求助"],
}

AGENTS = {
    ".claude/agents/qa-archaeologist.md": ["模块卡片", "接口清单", "01-系统认知"],
    ".claude/agents/qa-case-positive.md": ["正向", "做了该做的", "02-用例库"],
    ".claude/agents/qa-case-negative.md": ["破坏者", "逆向", "模式库"],
    ".claude/agents/qa-executor.md": ["checklist", "证据", "Allure"],
    ".claude/agents/qa-reporter.md": ["BUG 报告", "禅道", "周期汇报"],
}
COMMON_RUNTIME = [
    "开工先读知识库 00-索引.md", "只干职能内的事",
    "完整产物写入知识库文件，只回传摘要和产物路径", "从对话之间不通信",
]
ORCHESTRATOR_REQUIRED = [
    "qa-archaeologist", "qa-case-positive", "qa-case-negative", "qa-executor", "qa-reporter",
    "BUG 定级争议", "测试范围取舍", "不可逆动作", "合并去重", "复核",
    "摘要和产物路径", "没有证据=没完成",
]

problems: list[str] = []


def check(desc: str, ok: bool, detail: str = "") -> None:
    if not ok:
        problems.append(f"[{desc}] {detail}")


# 1) 结构
for f in EXPECTED_FILES:
    check("结构", (PKG / f).is_file(), f"缺少文件: {f}")

# 2) 模板
for rel, keys in REQUIRED_SECTIONS.items():
    p = PKG / rel
    if p.is_file():
        text = p.read_text(encoding="utf-8")
        for kw in keys:
            check("模板", kw in text, f"{rel} 缺字段: {kw}")

# 3) 从对话
for rel, keys in AGENTS.items():
    p = PKG / rel
    if not p.is_file():
        continue
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    check("从对话", bool(m), f"{rel} 缺 frontmatter")
    if m:
        check("从对话", "name:" in m.group(1), f"{rel} frontmatter 缺 name")
    for kw in COMMON_RUNTIME + keys:
        check("从对话", kw in text, f"{rel} 缺: {kw}")

# 4) 宪法
orch = PKG / "CLAUDE.md"
if orch.is_file():
    text = orch.read_text(encoding="utf-8")
    for kw in ORCHESTRATOR_REQUIRED:
        check("宪法", kw in text, f"CLAUDE.md 缺规则: {kw}")

for section in ["结构", "模板", "从对话", "宪法"]:
    n = sum(1 for p in problems if p.startswith(f"[{section}]"))
    print(f"{section}: {'通过' if n == 0 else f'{n} 项问题'}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("selfcheck 全部通过")
```

注意：`EXPECTED_FILES` 含 Task 6 的产物（html、部署手册）——**先创建两个占位文件**（`docs/2026-09-02-qa-test-workflow-design.html` 与 `docs/部署手册.md` 各写一行"Task 6 生成"），保证 selfcheck 在 Task 5 阶段可全绿；Task 6 用真内容覆盖占位文件。

同时创建 `qa-workflow/tools/install-batch1.ps1`：

```powershell
# QA 工作流第一批工具安装（Windows，管理员 PowerShell 执行）
# 第二/三批与 iOS 链路见设计文档第 8 节，按需再装
$ErrorActionPreference = "Stop"

Write-Host "== 1/5 k6（性能压测）=="
winget install --id GrafanaLabs.k6 -e

Write-Host "== 2/5 Allure 报告（allure-commandline，需 JRE）=="
scoop install allure 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "scoop 不可用，改用 npm: npm i -g allure-commandline"; npm i -g allure-commandline }

Write-Host "== 3/5 Schemathesis（契约+Fuzz，pytest 插件）=="
pip install schemathesis

Write-Host "== 4/5 禅道 MCP（官方 zentao-cli）=="
npm install -g zentao-cli
# 配置（手动一次）：setx ZENTAO_URL "https://<禅道地址>"
#                 setx ZENTAO_TOKEN "<个人设置-密钥生成的 token>"
# 或：zentao add-mcp 一键写入 Claude Code 配置

Write-Host "== 5/5 验证 =="
k6 version
allure --version
python -m schemathesis --version
zentao --version
Write-Host "第一批完成。Playwright 截图对比无需安装（已在栈内）。"
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest qa-workflow/tests/test_selfcheck.py qa-workflow/tests/test_structure.py -v`
Expected: PASS（含 test_structure，占位文件已使结构测试通过）

- [ ] **Step 5: Commit**

```bash
git add qa-workflow/scripts/ qa-workflow/tools/ qa-workflow/tests/test_selfcheck.py qa-workflow/docs/
git commit -m "qa-workflow: selfcheck 自检 + 第一批工具安装脚本"
```

---

### Task 6: 静态网页版设计文档 + 部署手册

**Files:**
- Create: `qa-workflow/docs/make_doc_html.py`（md→单文件 HTML 渲染脚本）
- Overwrite: `qa-workflow/docs/2026-09-02-qa-test-workflow-design.html`（替换占位）
- Overwrite: `qa-workflow/docs/部署手册.md`（替换占位）
- Create: `qa-workflow/tests/test_docs.py`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-09-02-qa-test-workflow-design.md`（源文档）
- Produces: 自包含 HTML（内嵌 CSS，无 CDN 依赖，内网可开）；`make_doc_html.py <输入.md> <输出.html>` 可复用渲染任何 md

- [ ] **Step 1: 写失败的渲染测试**

创建 `qa-workflow/tests/test_docs.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m pytest qa-workflow/tests/test_docs.py -v`
Expected: FAIL（脚本缺失/占位内容不全）

- [ ] **Step 3: 实现渲染脚本并生成 HTML**

先 `pip install markdown`（唯一新增依赖）。

创建 `qa-workflow/docs/make_doc_html.py`：

```python
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
<div class="watermark">© Raven Wang · 生成自 {src_md.name}</div>
</div></body>
</html>
"""
    dst_html.write_text(html, encoding="utf-8")
    print(f"OK: {dst_html} ({len(html)//1024} KB)")


if __name__ == "__main__":
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
```

生成 HTML（覆盖占位）：

```bash
python qa-workflow/docs/make_doc_html.py "docs/superpowers/specs/2026-09-02-qa-test-workflow-design.md" "qa-workflow/docs/2026-09-02-qa-test-workflow-design.html"
```

- [ ] **Step 4: 写部署手册（覆盖占位）**

`qa-workflow/docs/部署手册.md`：

```markdown
# QA 工作流包 · 部署手册

> © Raven Wang · 2026年09月02日
> 前提：目标机器 Windows 11、Claude Code 已装、Node 20+、Python 3.10+、JDK 17+（Maestro 用）

## 五步部署

1. **拷包**：整个 `qa-workflow/` 复制到目标机器工作目录（含被测项目源码仓的读写权）
2. **自检**：`python scripts/selfcheck.py`——输出"selfcheck 全部通过"才继续
3. **装工具**：管理员 PowerShell 跑 `tools/install-batch1.ps1`（k6/Allure/Schemathesis/zentao-cli）；
   然后配禅道环境变量 `ZENTAO_URL`、`ZENTAO_TOKEN`（或 `zentao add-mcp` 一键）；第二批（Maestro/mobile-mcp/Fastbot/Toxiproxy/ZAP）按设计文档第 8 节按需
4. **启用宪法与从对话**：把包内 `CLAUDE.md` 与 `.claude/` 放到工作目录根（包本身即此结构，直接在包根开 Claude Code 即可）
5. **冷启动**：按设计文档第 9 节——先选一个主路径模块（建议登录/配网），派考古从出第一张模块卡片，跑通"考古→双用例→执行→报告"最小闭环

## iOS 特别路径（有 Mac 前置）

Mac 上一次性编译签名 WDA 装入真机 → Windows `npm i -g go-ios`，`go-ios runwda` + 端口转发接管。Maestro 在 Windows 对 iOS 零能力，不要尝试。

## 验证部署成功的三条标准

- selfcheck 全绿
- 新开会话，主对话能复述"每轮八步编排 + 检查点三类"
- 禅道 MCP 能拉到一条真实工单（或提一条测试 bug 到测试产品再关闭）

## 常见问题

- 禅道老版本（API v1）：官方 zentao-cli 不可用，换 `npm i -g zentao-v1-mcp` 并改 MCP 配置，流程不变
- Allure 打不开中文路径：报告目录避免中文
- selfcheck 报文件缺失：git 拷贝时检查 `.claude/` 隐藏目录是否带上
```

- [ ] **Step 5: 运行全部测试确认通过**

Run: `python -m pytest qa-workflow/tests/ -v`
Expected: 全部 PASS（结构/模板/从对话/宪法/selfcheck/docs 六组）

人工验证（证据）：浏览器打开 `qa-workflow/docs/2026-09-02-qa-test-workflow-design.html`，截图留证（标题、表格样式、水印可见）。

- [ ] **Step 6: Commit**

```bash
git add qa-workflow/
git commit -m "qa-workflow: 静态网页版设计文档 + 部署手册，包完整交付"
```

---

## Self-Review 记录

- **Spec 覆盖**：spec §2 架构→Task 3/4；§3 知识库→Task 2；§4 双通道矩阵→Task 3（执行从/用例从职责内）+Task 4（编排第 5 步声明矩阵行）；§5 职能包→Task 3；§6 BUG 报告→Task 2 模板+Task 3 报告从/主对话复核；§7 汇报→Task 2 模板；§8 工具→Task 5 安装脚本（第一批）+部署手册（二三批指引）；§9 实施路线→部署手册冷启动；§10 风险→CLAUDE.md 重派规则/断点续跑。无遗漏。
- **占位符扫描**：Task 5 的两个占位文件是显式的过渡产物且 Task 6 覆盖，其余无 TBD/TODO。
- **类型/命名一致性**：agent 名（qa-archaeologist 等 5 个）在 Task 3 定义、Task 4 宪法引用、Task 5 selfcheck 校验，三处一致；模板文件名 Task 1 契约=Task 2 产出=Task 5 EXPECTED_FILES，一致。
