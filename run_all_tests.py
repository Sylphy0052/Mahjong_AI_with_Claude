#!/usr/bin/env python3
"""
全テストの統合実行ランナー

Poetry環境での実行:
poetry run python run_all_tests.py

または、個別テスト:
poetry run pytest tests/test_tile.py -v
poetry run pytest tests/test_hand.py -v
poetry run pytest tests/test_winning_checker.py -v
poetry run pytest tests/test_shanten_calculator.py -v
poetry run pytest tests/test_wall_tiles.py -v
poetry run pytest tests/test_game_engine.py -v
poetry run pytest tests/test_cui_interface.py -v
"""

import subprocess
import sys
from typing import List, Tuple


def run_command(command: List[str], description: str) -> Tuple[bool, str]:
    """コマンドを実行して結果を返す

    Args:
        command: 実行するコマンドのリスト
        description: コマンドの説明

    Returns:
        成功フラグとメッセージのタプル
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, f"✅ {description}: 成功"
    except subprocess.CalledProcessError as e:
        return False, f"❌ {description}: 失敗\n{e.stderr}"


def main() -> None:
    """メイン実行関数"""
    print("=" * 60)
    print("    麻雀AI Phase 1 - 全テスト実行")
    print("=" * 60)

    # テスト項目の定義
    test_items = [
        (["poetry", "run", "pytest", "tests/test_tile.py", "-v"], "牌クラステスト"),
        (["poetry", "run", "pytest", "tests/test_hand.py", "-v"], "手牌管理テスト"),
        (["poetry", "run", "pytest", "tests/test_winning_checker.py", "-v"], "和了判定テスト"),
        (["poetry", "run", "pytest", "tests/test_shanten_calculator.py", "-v"], "向聴数計算テスト"),
        (["poetry", "run", "pytest", "tests/test_wall_tiles.py", "-v"], "山牌管理テスト"),
        (["poetry", "run", "pytest", "tests/test_game_engine.py", "-v"], "ゲームエンジンテスト"),
        (["poetry", "run", "pytest", "tests/test_cui_interface.py", "-v"], "CUIインターフェーステスト"),
    ]

    # 結果記録
    results = []

    # 各テストを実行
    for command, description in test_items:
        print(f"\n{description}を実行中...")
        success, message = run_command(command, description)
        results.append((success, message))
        print(message)

    # 総合結果
    print("\n" + "=" * 60)
    print("    テスト結果サマリー")
    print("=" * 60)

    success_count = 0
    for success, message in results:
        print(message)
        if success:
            success_count += 1

    total_tests = len(results)
    print(f"\n総合結果: {success_count}/{total_tests} 成功")

    if success_count == total_tests:
        print("🎉 すべてのテストが成功しました！")
        sys.exit(0)
    else:
        print("❌ 一部のテストが失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
