#!/usr/bin/env python3
"""ツモ和了の選択制テスト"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.models.tile import Tile
from mahjong_ai.models.hand import Hand

def test_optional_win():
    """ツモ和了選択制のテスト"""
    print("=== ツモ和了選択制テスト ===")
    
    # GameEngineを初期化
    engine = GameEngine()
    
    # 和了直前の手牌を設定（13枚）
    test_tiles = [
        Tile("sou", 1), Tile("sou", 1), Tile("sou", 1),  # 刻子
        Tile("sou", 2), Tile("sou", 3), Tile("sou", 4),  # 順子
        Tile("sou", 5), Tile("sou", 6), Tile("sou", 7),  # 順子
        Tile("sou", 8), Tile("sou", 8), Tile("sou", 8),  # 刻子
        Tile("sou", 9)  # 雀頭の片方
    ]
    
    # 手牌を設定
    engine.current_hand = Hand(test_tiles)
    engine.game_state = GameState.PLAYER_TURN
    
    print(f"テスト手牌（13枚）: {engine.current_hand}")
    print(f"向聴数: {engine.calculate_shanten()}")
    
    # 和了牌をツモしてみる
    print("\n9索をツモして和了形にします...")
    winning_tile = Tile("sou", 9)
    
    # 手動でツモ処理をシミュレート
    engine.current_hand.add_tile(winning_tile)
    engine.last_drawn_tile = winning_tile
    engine.game_state = GameState.AFTER_DRAW
    
    print(f"ツモ後手牌（14枚）: {engine.current_hand}")
    print(f"ツモ牌: {engine.last_drawn_tile}")
    print(f"和了可能: {engine.can_win()}")
    print(f"向聴数: {engine.calculate_shanten()}")
    print(f"ゲーム状態: {engine.game_state}")
    print(f"和了判定: {engine.check_winning_hand()}")
    
    # 和了を実行してみる
    if engine.can_win():
        print(f"\n{engine.last_drawn_tile}でツモ和了を実行...")
        engine.execute_win(engine.last_drawn_tile)
        
        print(f"和了状態: {engine.is_winner}")
        print(f"和了牌: {engine.winning_tile}")
        print(f"ゲーム状態: {engine.game_state}")
    
    print("\n=== ツモ和了選択制テスト完了 ===")

def test_optional_win_after_kan():
    """暗槓後の嶺上開花選択制テスト"""
    print("\n=== 嶺上開花選択制テスト ===")
    
    engine = GameEngine()
    
    # 暗槓可能で、嶺上で和了する手牌
    test_tiles = [
        Tile("sou", 1), Tile("sou", 1), Tile("sou", 1), Tile("sou", 1),  # 暗槓用
        Tile("sou", 2), Tile("sou", 3), Tile("sou", 4),  # 順子
        Tile("sou", 5), Tile("sou", 6), Tile("sou", 7),  # 順子
        Tile("sou", 8), Tile("sou", 8), Tile("sou", 8),  # 刻子
        Tile("sou", 9)  # 雀頭の片方（9索がもう1枚来れば和了）
    ]
    
    engine.current_hand = Hand(test_tiles)
    engine.game_state = GameState.AFTER_DRAW
    
    print(f"暗槓前手牌: {engine.current_hand}")
    print(f"暗槓可能: {engine.can_kan()}")
    print(f"暗槓可能な牌: {engine.get_kan_possible_tiles()}")
    
    # 1索で暗槓実行
    target_tile = Tile("sou", 1)
    print(f"\n{target_tile}で暗槓実行...")
    
    # WallTilesの嶺上牌に9索を設定（テスト用）
    # 実際の実装では嶺上牌もランダムなので、ここでは結果を確認するだけ
    engine.execute_kan(target_tile)
    
    print(f"嶺上牌: {engine.last_drawn_tile}")
    print(f"和了可能: {engine.can_win()}")
    print(f"暗槓後手牌: {engine.current_hand}")
    print(f"ゲーム状態: {engine.game_state}")
    
    print("\n=== 嶺上開花選択制テスト完了 ===")

if __name__ == "__main__":
    test_optional_win()
    test_optional_win_after_kan()