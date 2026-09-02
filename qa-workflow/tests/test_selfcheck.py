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
