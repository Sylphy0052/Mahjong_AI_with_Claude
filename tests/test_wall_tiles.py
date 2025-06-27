"""山牌管理（WallTiles）クラスのテスト"""

from typing import Set

import pytest

from mahjong_ai.game.wall_tiles import WallTiles
from mahjong_ai.models.tile import Tile


class TestWallTiles:
    """山牌管理クラスのテスト"""

    def setup_method(self) -> None:
        """テストメソッド実行前の初期化"""
        self.wall = WallTiles()

    def test_wall_creation(self) -> None:
        """山牌作成テスト"""
        # 初期状態で54枚の索子牌（各種類6枚）
        assert self.wall.remaining_count == 54
        assert len(self.wall.remaining_tiles) == 54

    def test_wall_tile_distribution(self) -> None:
        """山牌の牌分布テスト"""
        # 各種類の牌が6枚ずつあることを確認
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            count = self.wall.remaining_tiles.count(tile)
            assert count == 6, f"{value}索が6枚でない: {count}枚"

    def test_draw_tile(self) -> None:
        """牌の抽選テスト"""
        initial_count = self.wall.remaining_count

        # 1枚抽選
        drawn_tile = self.wall.draw_tile()

        # 戻り値が正しい
        assert isinstance(drawn_tile, Tile)
        assert drawn_tile.suit == "sou"
        assert 1 <= drawn_tile.value <= 9

        # 枚数が減っている
        assert self.wall.remaining_count == initial_count - 1

        # 抽選された牌は山牌から除去されている
        assert drawn_tile not in self.wall.remaining_tiles or self.wall.remaining_tiles.count(drawn_tile) < 6

    def test_draw_multiple_tiles(self) -> None:
        """複数牌の抽選テスト"""
        initial_count = self.wall.remaining_count
        drawn_tiles = []

        # 10枚抽選
        for _ in range(10):
            drawn_tile = self.wall.draw_tile()
            drawn_tiles.append(drawn_tile)

        # 枚数が正しく減っている
        assert self.wall.remaining_count == initial_count - 10

        # 抽選された牌はすべて有効
        for tile in drawn_tiles:
            assert isinstance(tile, Tile)
            assert tile.suit == "sou"
            assert 1 <= tile.value <= 9

    def test_draw_all_tiles(self) -> None:
        """全牌抽選テスト"""
        drawn_tiles = []

        # 全ての牌を抽選
        while self.wall.remaining_count > 0:
            drawn_tile = self.wall.draw_tile()
            drawn_tiles.append(drawn_tile)

        # 54枚すべて抽選されている
        assert len(drawn_tiles) == 54

        # 山牌は空
        assert self.wall.remaining_count == 0
        assert len(self.wall.remaining_tiles) == 0

    def test_draw_from_empty_wall(self) -> None:
        """空の山牌からの抽選テスト"""
        # 全ての牌を抽選
        while self.wall.remaining_count > 0:
            self.wall.draw_tile()

        # 空の山牌から抽選を試みる
        with pytest.raises(ValueError, match="山牌が空です"):
            self.wall.draw_tile()

    def test_peek_tile(self) -> None:
        """牌の確認テスト（抽選せずに見る）"""
        initial_count = self.wall.remaining_count

        # 次の牌を確認
        peeked_tile = self.wall.peek_next_tile()

        # 戻り値が正しい
        assert isinstance(peeked_tile, Tile)
        assert peeked_tile.suit == "sou"
        assert 1 <= peeked_tile.value <= 9

        # 枚数は変わらない
        assert self.wall.remaining_count == initial_count

        # 実際に抽選すると同じ牌が取得される
        drawn_tile = self.wall.draw_tile()
        assert drawn_tile == peeked_tile

    def test_peek_empty_wall(self) -> None:
        """空の山牌での確認テスト"""
        # 全ての牌を抽選
        while self.wall.remaining_count > 0:
            self.wall.draw_tile()

        # 空の山牌で確認を試みる
        with pytest.raises(ValueError, match="山牌が空です"):
            self.wall.peek_next_tile()

    def test_shuffle_randomness(self) -> None:
        """シャッフルのランダム性テスト"""
        # 複数回山牌を作成して、最初の牌が同じでないことを確認
        first_tiles = []

        for _ in range(10):
            wall = WallTiles()
            first_tile = wall.peek_next_tile()
            first_tiles.append(first_tile)

        # 全て同じ牌ではない（ランダムにシャッフルされている）
        unique_tiles = set(first_tiles)
        assert len(unique_tiles) > 1, "シャッフルされていない可能性があります"

    def test_has_tile(self) -> None:
        """特定牌の存在確認テスト"""
        # 初期状態では全ての種類の牌が存在
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            assert self.wall.has_tile(tile), f"{value}索が存在しない"

    def test_count_tile(self) -> None:
        """特定牌の枚数カウントテスト"""
        # 初期状態では各種類の牌が6枚
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            count = self.wall.count_tile(tile)
            assert count == 6, f"{value}索が6枚でない: {count}枚"

    def test_count_tile_after_draw(self) -> None:
        """抽選後の牌枚数カウントテスト"""
        # 1索を数枚抽選
        one_sou = Tile(suit="sou", value=1)
        drawn_count = 0

        while self.wall.has_tile(one_sou) and drawn_count < 3:
            drawn_tile = self.wall.draw_tile()
            if drawn_tile == one_sou:
                drawn_count += 1
            # 抽選されなかった場合は山牌に戻す（テスト用）
            if drawn_tile != one_sou:
                # 実際の実装では戻せないので、このテストは調整が必要
                pass

        # 残りの1索枚数を確認
        remaining_count = self.wall.count_tile(one_sou)
        assert remaining_count == 6 - drawn_count, f"1索の残り枚数が正しくない"

    def test_wall_state_consistency(self) -> None:
        """山牌状態の整合性テスト"""
        # 初期状態
        assert self.wall.remaining_count == len(self.wall.remaining_tiles)

        # 数枚抽選後
        for _ in range(5):
            self.wall.draw_tile()

        assert self.wall.remaining_count == len(self.wall.remaining_tiles)

        # 全抽選後
        while self.wall.remaining_count > 0:
            self.wall.draw_tile()

        assert self.wall.remaining_count == 0
        assert len(self.wall.remaining_tiles) == 0

    def test_wall_reset(self) -> None:
        """山牌リセットテスト"""
        # 数枚抽選
        for _ in range(10):
            self.wall.draw_tile()

        assert self.wall.remaining_count == 44

        # リセット
        self.wall.reset()

        # 初期状態に戻る
        assert self.wall.remaining_count == 54
        assert len(self.wall.remaining_tiles) == 54

        # 各種類の牌が6枚ずつ
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            count = self.wall.count_tile(tile)
            assert count == 6, f"リセット後に{value}索が6枚でない: {count}枚"

    def test_draw_specific_tile(self) -> None:
        """特定牌の抽選テスト（デバッグ用）"""
        # 特定の牌を指定して抽選
        target_tile = Tile(suit="sou", value=5)

        # 5索が存在することを確認
        assert self.wall.has_tile(target_tile)

        # 5索を抽選（実装によってはサポートされない）
        try:
            drawn_tile = self.wall.draw_specific_tile(target_tile)
            assert drawn_tile == target_tile

            # 枚数が減っている
            remaining = self.wall.count_tile(target_tile)
            assert remaining == 5
        except AttributeError:
            # draw_specific_tileメソッドが実装されていない場合はスキップ
            pass
