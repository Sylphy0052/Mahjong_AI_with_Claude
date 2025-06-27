#!/usr/bin/env python3
"""暗槓機能のテスト"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.models.tile import Tile
from mahjong_ai.models.hand import Hand

def test_kan_functionality():
    """暗槓機能のテスト"""
    print("=== 暗槓機能テスト ===")
    
    # GameEngineを初期化
    engine = GameEngine()
    print(f"初期状態: {engine.game_state}")
    
    # テスト用手牌を設定（1索が4枚、その他で10枚）
    test_tiles = [
        Tile("sou", 1), Tile("sou", 1), Tile("sou", 1), Tile("sou", 1),  # 暗槓用
        Tile("sou", 2), Tile("sou", 3), Tile("sou", 4),  # 順子用
        Tile("sou", 5), Tile("sou", 6), Tile("sou", 7),  # 順子用
        Tile("sou", 8), Tile("sou", 8), Tile("sou", 8),  # 刻子用
        Tile("sou", 9)  # ツモ後14枚目
    ]
    
    # 手牌を直接設定
    engine.current_hand = Hand(test_tiles)
    engine.game_state = GameState.AFTER_DRAW
    
    print(f"テスト手牌: {engine.current_hand}")
    print(f"手牌枚数: {engine.current_hand.size}")
    
    # 暗槓可能な牌を取得
    kan_tiles = engine.get_kan_possible_tiles()
    print(f"暗槓可能な牌: {kan_tiles}")
    
    # 暗槓可能かチェック
    can_kan = engine.can_kan()
    print(f"暗槓可能: {can_kan}")
    
    if can_kan and kan_tiles:
        # 1索で暗槓を実行
        target_tile = Tile("sou", 1)
        print(f"\n{target_tile}で暗槓を実行...")
        
        # 暗槓前の状態
        print(f"暗槓前手牌: {engine.current_hand}")
        print(f"暗槓前手牌枚数: {engine.current_hand.size}")
        print(f"暗槓前状態: {engine.game_state}")
        
        try:
            engine.execute_kan(target_tile)
            
            # 暗槓後の状態
            print(f"暗槓後手牌: {engine.current_hand}")
            print(f"暗槓後手牌枚数: {engine.current_hand.size}")
            print(f"暗槓後状態: {engine.game_state}")
            print(f"暗槓牌: {engine.kan_tiles}")
            print(f"和了状態: {engine.is_winner}")
            
            # 嶺上牌の残り枚数を確認
            print(f"嶺上牌残り: {engine.wall.rinshan_count}")
            
        except Exception as e:
            print(f"エラー: {e}")
    
    print("\n=== 暗槓機能テスト完了 ===")

def test_kan_conditions():
    """暗槓条件のテスト"""
    print("\n=== 暗槓条件テスト ===")
    
    engine = GameEngine()
    
    # 1. 同じ牌が4枚ない場合（暗槓不可）
    test_tiles = [Tile("sou", i) for i in range(1, 10)] + [Tile("sou", i) for i in range(1, 5)]
    engine.current_hand = Hand(test_tiles)
    engine.game_state = GameState.AFTER_DRAW
    
    print(f"テスト1: 4枚揃わない場合")
    print(f"手牌: {engine.current_hand}")
    print(f"暗槓可能: {engine.can_kan()}")
    print(f"暗槓可能な牌: {engine.get_kan_possible_tiles()}")
    
    # 2. リーチ中の場合（暗槓不可）
    test_tiles = [Tile("sou", 1)] * 4 + [Tile("sou", i) for i in range(2, 10)] + [Tile("sou", 9)] * 2
    engine.current_hand = Hand(test_tiles)
    engine.game_state = GameState.AFTER_DRAW
    engine.is_riichi = True
    
    print(f"\nテスト2: リーチ中の場合")
    print(f"手牌: {engine.current_hand}")
    print(f"リーチ状態: {engine.is_riichi}")
    print(f"暗槓可能: {engine.can_kan()}")
    print(f"暗槓可能な牌: {engine.get_kan_possible_tiles()}")
    
    print("\n=== 暗槓条件テスト完了 ===")

if __name__ == "__main__":
    test_kan_functionality()
    test_kan_conditions()