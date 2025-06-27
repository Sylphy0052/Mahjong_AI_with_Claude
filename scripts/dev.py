#!/usr/bin/env python3
"""開発用スクリプト - Poetry環境での開発ツール実行"""

import os
import subprocess
import sys


def run_command(cmd: list[str], description: str) -> bool:
    """コマンドを実行し、結果を表示"""
    print(f"\n=== {description} ===")
    print(f"実行コマンド: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, cwd=os.getcwd())
        print(f"OK {description} - 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"NG {description} - 失敗 (終了コード: {e.returncode})")
        return False


def main():
    """開発ツールを実行"""

    commands = [
        (["poetry", "run", "pytest", "-v"], "テスト実行"),
        (["poetry", "run", "black", "--check", "src", "tests"], "Black フォーマットチェック"),
        (["poetry", "run", "isort", "--check-only", "src", "tests"], "isort インポート順序チェック"),
        (["poetry", "run", "flake8", "src", "tests"], "flake8 リントチェック"),
        (["poetry", "run", "mypy", "src"], "mypy 型チェック"),
    ]

    success_count = 0
    for cmd, description in commands:
        if run_command(cmd, description):
            success_count += 1

    print(f"\n=== 結果 ===")
    print(f"成功: {success_count}/{len(commands)}")

    if success_count == len(commands):
        print("OK すべてのチェックが成功しました！")
        sys.exit(0)
    else:
        print("NG 一部のチェックが失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
