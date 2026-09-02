# QA 工作流第一批工具安装（Windows，管理员 PowerShell 执行）
# 第二/三批与 iOS 链路见设计文档第 8 节，按需再装
$ErrorActionPreference = "Stop"

Write-Host "== 1/5 k6（性能压测）=="
winget install --id GrafanaLabs.k6 -e

Write-Host "== 2/5 Allure 报告（allure-commandline，需 JRE）=="
if (Get-Command scoop -ErrorAction SilentlyContinue) { scoop install allure } else { Write-Host "scoop 不可用，改用 npm: npm i -g allure-commandline"; npm i -g allure-commandline }

Write-Host "== 3/5 Schemathesis（契约+Fuzz，pytest 插件）=="
pip install schemathesis allure-pytest

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
