#!/usr/bin/env python3
"""
簡易テストランナー（Poetry環境用）

個別実行例:
poetry run python scripts/test_simple.py tile
poetry run python scripts/test_simple.py hand
poetry run python scripts/test_simple.py winning
poetry run python scripts/test_simple.py shanten
poetry run python scripts/test_simple.py wall
poetry run python scripts/test_simple.py engine
poetry run python scripts/test_simple.py cui
poetry run python scripts/test_simple.py all
"""

import sys
from typing import Optional

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.game.wall_tiles import WallTiles
from mahjong_ai.interface.cui_interface import CUIInterface
from mahjong_ai.logic.shanten_calculator import ShantenCalculator
from mahjong_ai.logic.winning_checker import WinningChecker
from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


def test_tile() -> bool:
    """牌クラスの簡易テスト"""
    print("=== 牌クラステスト ===")

    # 基本作成
    tile1 = Tile(suit="sou", value=1)
    tile2 = Tile(suit="sou", value=2)
    tile3 = Tile(suit="sou", value=1)

    # 比較テスト
    assert tile1 != tile2, "異なる牌の比較"
    assert tile1 == tile3, "同じ牌の比較"
    assert tile1 < tile2, "牌のソート"

    # 文字列表現
    assert str(tile1) == "1索", "文字列表現"

    print("✅ 牌クラステスト成功")
    return True


def test_hand() -> bool:
    """手牌クラスの簡易テスト"""
    print("=== 手牌クラステスト ===")

    hand = Hand()
    assert hand.size == 0, "初期サイズ"

    # 牌追加
    tiles = [Tile(suit="sou", value=i) for i in [3, 1, 2]]
    for tile in tiles:
        hand.add_tile(tile)

    # ソート確認
    sorted_values = [tile.value for tile in hand.tiles]
    assert sorted_values == [1, 2, 3], "自動ソート"

    # 牌除去
    hand.remove_tile(Tile(suit="sou", value=2))
    assert hand.size == 2, "牌除去後のサイズ"

    print("✅ 手牌クラステスト成功")
    return True


def test_winning() -> bool:
    """和了判定の簡易テスト"""
    print("=== 和了判定テスト ===")

    checker = WinningChecker()

    # 七対子テスト
    tiles = []
    for value in range(1, 8):
        tiles.extend([Tile(suit="sou", value=value), Tile(suit="sou", value=value)])

    hand = Hand(tiles)
    assert checker.is_winning_hand(hand), "七対子和了判定"

    # 通常形テスト
    tiles = [
        # 1索刻子
        Tile(suit="sou", value=1),
        Tile(suit="sou", value=1),
        Tile(suit="sou", value=1),
        # 2索刻子
        Tile(suit="sou", value=2),
        Tile(suit="sou", value=2),
        Tile(suit="sou", value=2),
        # 3索刻子
        Tile(suit="sou", value=3),
        Tile(suit="sou", value=3),
        Tile(suit="sou", value=3),
        # 4索刻子
        Tile(suit="sou", value=4),
        Tile(suit="sou", value=4),
        Tile(suit="sou", value=4),
        # 5索対子（雀頭）
        Tile(suit="sou", value=5),
        Tile(suit="sou", value=5),
    ]
    hand = Hand(tiles)
    assert checker.is_winning_hand(hand), "通常形和了判定"

    print("✅ 和了判定テスト成功")
    return True


def test_shanten() -> bool:
    """向聴数計算の簡易テスト"""
    print("=== 向聴数計算テスト ===")

    calculator = ShantenCalculator()

    # 和了形テスト
    tiles = []
    for value in range(1, 8):
        tiles.extend([Tile(suit="sou", value=value), Tile(suit="sou", value=value)])

    hand = Hand(tiles)
    shanten = calculator.calculate_shanten(hand)
    assert shanten == -1, "和了形の向聴数"

    print("✅ 向聴数計算テスト成功")
    return True


def test_wall() -> bool:
    """山牌管理の簡易テスト"""
    print("=== 山牌管理テスト ===")

    wall = WallTiles()
    assert wall.remaining_count == 54, "初期山牌数"

    # 抽選テスト
    drawn = wall.draw_tile()
    assert isinstance(drawn, Tile), "抽選牌がTileインスタンス"
    assert wall.remaining_count == 53, "抽選後の山牌数"

    print("✅ 山牌管理テスト成功")
    return True


def test_engine() -> bool:
    """ゲームエンジンの簡易テスト"""
    print("=== ゲームエンジンテスト ===")

    engine = GameEngine()
    assert engine.game_state == GameState.NOT_STARTED, "初期状態"

    # ゲーム開始
    engine.start_game()
    assert engine.game_state == GameState.PLAYER_TURN, "開始後状態"
    assert engine.current_hand.size == 13, "初期手牌"

    # ツモ
    drawn = engine.draw_tile()
    assert engine.current_hand.size == 14, "ツモ後手牌"
    assert engine.game_state == GameState.AFTER_DRAW, "ツモ後状態"

    print("✅ ゲームエンジンテスト成功")
    return True


def test_cui() -> bool:
    """CUIインターフェースの簡易テスト"""
    print("=== CUIインターフェーステスト ===")

    interface = CUIInterface()
    assert interface.engine.game_state == GameState.NOT_STARTED, "CUI初期状態"

    # 状態説明テスト
    description = interface.get_state_description()
    assert description == "未開始", "状態説明"

    print("✅ CUIインターフェーステスト成功")
    return True


def run_all_tests() -> bool:
    """全テストを実行"""
    tests = [
        ("牌クラス", test_tile),
        ("手牌管理", test_hand),
        ("和了判定", test_winning),
        ("向聴数計算", test_shanten),
        ("山牌管理", test_wall),
        ("ゲームエンジン", test_engine),
        ("CUIインターフェース", test_cui),
    ]

    print("=" * 50)
    print("    麻雀AI Phase 1 - 全テスト実行")
    print("=" * 50)

    success_count = 0
    for name, test_func in tests:
        try:
            test_func()
            success_count += 1
        except Exception as e:
            print(f"❌ {name}テスト失敗: {e}")

    print(f"\n総合結果: {success_count}/{len(tests)} 成功")

    if success_count == len(tests):
        print("🎉 すべてのテストが成功しました！")
        return True
    else:
        print("❌ 一部のテストが失敗しました。")
        return False


def main() -> None:
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: poetry run python scripts/test_simple.py <test_name>")
        print("利用可能なテスト: tile, hand, winning, shanten, wall, engine, cui, all")
        sys.exit(1)

    test_name = sys.argv[1].lower()

    test_map = {
        "tile": test_tile,
        "hand": test_hand,
        "winning": test_winning,
        "shanten": test_shanten,
        "wall": test_wall,
        "engine": test_engine,
        "cui": test_cui,
        "all": run_all_tests,
    }

    if test_name not in test_map:
        print(f"不明なテスト: {test_name}")
        print("利用可能なテスト: " + ", ".join(test_map.keys()))
        sys.exit(1)

    try:
        success = test_map[test_name]()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"テスト実行エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
