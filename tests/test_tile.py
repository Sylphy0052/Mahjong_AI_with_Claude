"""牌（Tile）クラスのテスト"""

from dataclasses import FrozenInstanceError

import pytest

from mahjong_ai.models.tile import Tile


class TestTile:
    """牌クラスのテスト"""

    def test_tile_creation_valid(self) -> None:
        """正常な牌の作成テスト"""
        tile = Tile(suit="sou", value=1)
        assert tile.suit == "sou"
        assert tile.value == 1

    def test_tile_creation_all_values(self) -> None:
        """すべての有効な値での牌作成テスト"""
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            assert tile.suit == "sou"
            assert tile.value == value

    def test_tile_immutable(self) -> None:
        """牌のイミュータブル性テスト"""
        tile = Tile(suit="sou", value=5)

        # 値の変更を試みると例外が発生
        with pytest.raises(FrozenInstanceError):
            tile.suit = "man"  # type: ignore

        with pytest.raises(FrozenInstanceError):
            tile.value = 3  # type: ignore

    def test_tile_equality(self) -> None:
        """牌の等価性テスト"""
        tile1 = Tile(suit="sou", value=5)
        tile2 = Tile(suit="sou", value=5)
        tile3 = Tile(suit="sou", value=3)

        assert tile1 == tile2
        assert tile1 != tile3
        assert hash(tile1) == hash(tile2)
        assert hash(tile1) != hash(tile3)

    def test_tile_string_representation(self) -> None:
        """牌の文字列表現テスト"""
        tile = Tile(suit="sou", value=5)
        assert str(tile) == "5索"

        # 各数字での表現確認
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            assert str(tile) == f"{value}索"

    def test_tile_repr(self) -> None:
        """牌のrepr表現テスト"""
        tile = Tile(suit="sou", value=5)
        expected = "Tile(suit='sou', value=5)"
        assert repr(tile) == expected

    def test_tile_id_property(self) -> None:
        """牌IDプロパティのテスト"""
        # 索子のID範囲: 0-8 (value 1-9)
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            expected_id = value - 1  # 1索→0, 2索→1, ..., 9索→8
            assert tile.tile_id == expected_id

    def test_tile_ordering(self) -> None:
        """牌の順序比較テスト"""
        tile1 = Tile(suit="sou", value=1)
        tile2 = Tile(suit="sou", value=5)
        tile3 = Tile(suit="sou", value=9)

        assert tile1 < tile2 < tile3
        assert tile3 > tile2 > tile1
        assert tile1 <= tile2 <= tile3
        assert tile3 >= tile2 >= tile1

    def test_tile_sorting(self) -> None:
        """牌のソートテスト"""
        tiles = [
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=3),
        ]

        sorted_tiles = sorted(tiles)
        expected_values = [1, 3, 5, 9]

        for tile, expected_value in zip(sorted_tiles, expected_values):
            assert tile.value == expected_value

    def test_tile_creation_invalid_suit(self) -> None:
        """不正なスート（種類）での牌作成テスト"""
        with pytest.raises(ValueError, match="Phase 1では索子のみサポート"):
            Tile(suit="man", value=5)

        with pytest.raises(ValueError, match="Phase 1では索子のみサポート"):
            Tile(suit="pin", value=5)

    def test_tile_creation_invalid_value(self) -> None:
        """不正な値での牌作成テスト"""
        with pytest.raises(ValueError, match="索子の値は1-9である必要があります"):
            Tile(suit="sou", value=0)

        with pytest.raises(ValueError, match="索子の値は1-9である必要があります"):
            Tile(suit="sou", value=10)

        with pytest.raises(ValueError, match="索子の値は1-9である必要があります"):
            Tile(suit="sou", value=-1)

    def test_tile_is_terminal(self) -> None:
        """么九牌（1, 9）の判定テスト"""
        tile_1 = Tile(suit="sou", value=1)
        tile_5 = Tile(suit="sou", value=5)
        tile_9 = Tile(suit="sou", value=9)

        assert tile_1.is_terminal
        assert not tile_5.is_terminal
        assert tile_9.is_terminal

    def test_tile_is_middle(self) -> None:
        """中張牌（2-8）の判定テスト"""
        tile_1 = Tile(suit="sou", value=1)
        tile_5 = Tile(suit="sou", value=5)
        tile_9 = Tile(suit="sou", value=9)

        assert not tile_1.is_middle
        assert tile_5.is_middle
        assert not tile_9.is_middle
