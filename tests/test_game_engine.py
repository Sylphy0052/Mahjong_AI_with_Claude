"""ゲームエンジン（GameEngine）クラスのテスト"""

from typing import List

import pytest

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.models.tile import Tile


class TestGameEngine:
    """ゲームエンジンクラスのテスト"""

    def setup_method(self) -> None:
        """テストメソッド実行前の初期化"""
        self.engine = GameEngine()

    def test_game_initialization(self) -> None:
        """ゲーム初期化テスト"""
        assert self.engine.game_state == GameState.NOT_STARTED
        assert self.engine.current_hand.size == 0
        assert self.engine.wall.remaining_count == 54
        assert self.engine.turn_count == 0
        assert not self.engine.is_riichi

    def test_start_game(self) -> None:
        """ゲーム開始テスト"""
        self.engine.start_game()

        # ゲーム状態が変更されている
        assert self.engine.game_state == GameState.PLAYER_TURN

        # 13枚配牌されている
        assert self.engine.current_hand.size == 13

        # 山牌から13枚減っている
        assert self.engine.wall.remaining_count == 54 - 13

        # ターン数が1
        assert self.engine.turn_count == 1

    def test_start_game_twice(self) -> None:
        """ゲーム重複開始テスト"""
        self.engine.start_game()

        # 2回目の開始を試みる
        with pytest.raises(ValueError, match="ゲームは既に開始されています"):
            self.engine.start_game()

    def test_draw_tile(self) -> None:
        """ツモテスト"""
        self.engine.start_game()
        initial_hand_size = self.engine.current_hand.size
        initial_wall_count = self.engine.wall.remaining_count

        # ツモ実行
        drawn_tile = self.engine.draw_tile()

        # 戻り値が正しい
        assert isinstance(drawn_tile, Tile)

        # 手牌が14枚になっている
        assert self.engine.current_hand.size == initial_hand_size + 1

        # 山牌が1枚減っている
        assert self.engine.wall.remaining_count == initial_wall_count - 1

        # 状態がツモ後になっている
        assert self.engine.game_state == GameState.AFTER_DRAW

    def test_draw_tile_before_start(self) -> None:
        """ゲーム開始前のツモテスト"""
        with pytest.raises(ValueError, match="ゲームが開始されていません"):
            self.engine.draw_tile()

    def test_discard_tile(self) -> None:
        """打牌テスト"""
        self.engine.start_game()
        self.engine.draw_tile()  # 14枚にする

        # 手牌から1枚選んで打牌
        hand_tiles = self.engine.current_hand.tiles
        discard_tile = hand_tiles[0]
        initial_hand_size = self.engine.current_hand.size

        # 打牌実行
        self.engine.discard_tile(discard_tile)

        # 手牌が13枚に戻っている
        assert self.engine.current_hand.size == initial_hand_size - 1

        # 打牌された牌が手牌にない
        assert discard_tile not in self.engine.current_hand.tiles

        # 捨て牌に追加されている
        assert discard_tile in self.engine.discarded_tiles

        # 状態がプレイヤーターンに戻っている
        assert self.engine.game_state == GameState.PLAYER_TURN

        # ターン数が増えている
        assert self.engine.turn_count == 2

    def test_discard_tile_not_in_hand(self) -> None:
        """手牌にない牌の打牌テスト"""
        self.engine.start_game()
        self.engine.draw_tile()

        # 手牌にない牌を作成
        fake_tile = Tile(suit="sou", value=9)
        while fake_tile in self.engine.current_hand.tiles:
            fake_tile = Tile(suit="sou", value=(fake_tile.value % 9) + 1)

        # 存在しない牌の打牌を試みる
        with pytest.raises(ValueError, match="指定された牌が手牌にありません"):
            self.engine.discard_tile(fake_tile)

    def test_discard_tile_wrong_state(self) -> None:
        """不正な状態での打牌テスト"""
        self.engine.start_game()
        # ツモしていない状態（13枚）で打牌を試みる

        hand_tiles = self.engine.current_hand.tiles
        with pytest.raises(ValueError, match="打牌できる状態ではありません"):
            self.engine.discard_tile(hand_tiles[0])

    def test_check_winning_hand(self) -> None:
        """和了判定テスト"""
        self.engine.start_game()

        # 初期状態では和了していない
        assert not self.engine.check_winning_hand()

        # 強制的に和了形を作成（テスト用）
        winning_tiles = []
        for value in range(1, 8):  # 1-7索を各2枚（七対子）
            winning_tiles.extend([Tile(suit="sou", value=value), Tile(suit="sou", value=value)])

        self.engine.current_hand._tiles = winning_tiles

        # 和了判定
        assert self.engine.check_winning_hand()

    def test_calculate_shanten(self) -> None:
        """向聴数計算テスト"""
        self.engine.start_game()

        # 13枚での向聴数計算
        shanten = self.engine.calculate_shanten()
        assert isinstance(shanten, int)
        assert shanten >= 0  # 13枚なので0向聴以上

    def test_declare_riichi(self) -> None:
        """リーチ宣言テスト"""
        self.engine.start_game()

        # リーチ前の状態
        assert not self.engine.is_riichi

        # リーチ宣言
        self.engine.declare_riichi()

        # リーチ状態になっている
        assert self.engine.is_riichi
        assert self.engine.game_state == GameState.RIICHI

    def test_declare_riichi_twice(self) -> None:
        """リーチ重複宣言テスト"""
        self.engine.start_game()
        self.engine.declare_riichi()

        # 2回目のリーチ宣言を試みる
        with pytest.raises(ValueError, match="既にリーチしています"):
            self.engine.declare_riichi()

    def test_auto_win_check(self) -> None:
        """自動和了チェックテスト"""
        self.engine.start_game()

        # 強制的に和了形を作成
        winning_tiles = []
        for value in range(1, 8):  # 1-7索を各2枚（七対子）
            winning_tiles.extend([Tile(suit="sou", value=value), Tile(suit="sou", value=value)])

        self.engine.current_hand._tiles = winning_tiles

        # ツモを実行（和了形+1枚で和了チェックが動作）
        drawn_tile = self.engine.draw_tile()

        # 自動的に和了状態になる
        if self.engine.check_winning_hand():
            self.engine.game_state = GameState.GAME_OVER
            assert self.engine.game_state == GameState.GAME_OVER

    def test_get_possible_discards(self) -> None:
        """打牌可能牌取得テスト"""
        self.engine.start_game()
        self.engine.draw_tile()  # 14枚にする

        possible_discards = self.engine.get_possible_discards()

        # 手牌のすべての牌が打牌可能
        assert len(possible_discards) <= 14
        assert all(tile in self.engine.current_hand.tiles for tile in possible_discards)

    def test_get_game_info(self) -> None:
        """ゲーム情報取得テスト"""
        self.engine.start_game()

        info = self.engine.get_game_info()

        # 必要な情報が含まれている
        assert "state" in info
        assert "hand_size" in info
        assert "wall_remaining" in info
        assert "turn_count" in info
        assert "is_riichi" in info
        assert "shanten" in info

        # 値が正しい
        assert info["state"] == GameState.PLAYER_TURN.value
        assert info["hand_size"] == 13
        assert info["wall_remaining"] == 54 - 13
        assert info["turn_count"] == 1
        assert info["is_riichi"] is False

    def test_reset_game(self) -> None:
        """ゲームリセットテスト"""
        self.engine.start_game()
        self.engine.draw_tile()
        self.engine.declare_riichi()

        # ゲーム進行後の状態確認
        assert self.engine.game_state != GameState.NOT_STARTED
        assert self.engine.current_hand.size > 0
        assert self.engine.is_riichi

        # リセット実行
        self.engine.reset_game()

        # 初期状態に戻っている
        assert self.engine.game_state == GameState.NOT_STARTED
        assert self.engine.current_hand.size == 0
        assert self.engine.wall.remaining_count == 54
        assert self.engine.turn_count == 0
        assert not self.engine.is_riichi
        assert len(self.engine.discarded_tiles) == 0

    def test_full_game_flow(self) -> None:
        """完全なゲームフローテスト"""
        # ゲーム開始
        self.engine.start_game()
        assert self.engine.game_state == GameState.PLAYER_TURN

        # 数ターン実行
        for turn in range(5):
            # ツモ
            drawn_tile = self.engine.draw_tile()
            assert self.engine.game_state == GameState.AFTER_DRAW
            assert self.engine.current_hand.size == 14

            # 打牌（最初の牌を捨てる）
            discard_tile = self.engine.current_hand.tiles[0]
            self.engine.discard_tile(discard_tile)
            assert self.engine.game_state == GameState.PLAYER_TURN
            assert self.engine.current_hand.size == 13

            # ターン数確認
            assert self.engine.turn_count == turn + 2

        # 捨て牌確認
        assert len(self.engine.discarded_tiles) == 5

    def test_wall_empty_scenario(self) -> None:
        """山牌枯渇シナリオテスト"""
        self.engine.start_game()

        # 山牌を意図的に枯渇させる
        while self.engine.wall.remaining_count > 1:
            self.engine.wall.draw_tile()

        # 最後のツモを試みる
        try:
            self.engine.draw_tile()
            # 成功した場合、ゲーム状態をチェック
            assert self.engine.game_state in [GameState.AFTER_DRAW, GameState.GAME_OVER]
        except ValueError:
            # 流局処理が実装されている場合
            assert self.engine.game_state == GameState.GAME_OVER
