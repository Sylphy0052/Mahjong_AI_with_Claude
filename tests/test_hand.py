"""手牌（Hand）クラスのテスト"""

import pytest

from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


class TestHand:
    """手牌クラスのテスト"""

    def test_hand_creation_empty(self) -> None:
        """空の手牌作成テスト"""
        hand = Hand()
        assert len(hand.tiles) == 0
        assert hand.size == 0

    def test_hand_creation_with_tiles(self) -> None:
        """牌を指定した手牌作成テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)

        assert hand.size == 3
        # 自動的にソートされることを確認
        expected_values = [1, 3, 5]
        for tile, expected_value in zip(hand.tiles, expected_values):
            assert tile.value == expected_value

    def test_hand_add_tile(self) -> None:
        """牌の追加テスト"""
        hand = Hand()
        tile1 = Tile(suit="sou", value=5)
        tile2 = Tile(suit="sou", value=2)
        tile3 = Tile(suit="sou", value=8)

        hand.add_tile(tile1)
        assert hand.size == 1
        assert hand.tiles[0] == tile1

        hand.add_tile(tile2)
        assert hand.size == 2
        # ソート順を確認（2索, 5索）
        assert hand.tiles[0].value == 2
        assert hand.tiles[1].value == 5

        hand.add_tile(tile3)
        assert hand.size == 3
        # ソート順を確認（2索, 5索, 8索）
        expected_values = [2, 5, 8]
        for tile, expected_value in zip(hand.tiles, expected_values):
            assert tile.value == expected_value

    def test_hand_remove_tile(self) -> None:
        """牌の除去テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=3),  # 重複あり
        ]
        hand = Hand(tiles)

        # 3索を1枚除去
        tile_to_remove = Tile(suit="sou", value=3)
        hand.remove_tile(tile_to_remove)

        assert hand.size == 3
        # 1つの3索のみが除去されることを確認
        values = [tile.value for tile in hand.tiles]
        assert values == [1, 3, 5]

    def test_hand_remove_tile_not_found(self) -> None:
        """存在しない牌の除去テスト"""
        tiles = [Tile(suit="sou", value=1), Tile(suit="sou", value=3)]
        hand = Hand(tiles)

        with pytest.raises(ValueError, match="指定された牌が手牌に存在しません"):
            hand.remove_tile(Tile(suit="sou", value=5))

    def test_hand_has_tile(self) -> None:
        """牌の存在確認テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)

        assert hand.has_tile(Tile(suit="sou", value=1))
        assert hand.has_tile(Tile(suit="sou", value=3))
        assert not hand.has_tile(Tile(suit="sou", value=5))

    def test_hand_count_tile(self) -> None:
        """牌の枚数カウントテスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)

        assert hand.count_tile(Tile(suit="sou", value=1)) == 1
        assert hand.count_tile(Tile(suit="sou", value=3)) == 3
        assert hand.count_tile(Tile(suit="sou", value=5)) == 0

    def test_hand_tiles_immutable(self) -> None:
        """hand.tilesが読み取り専用であることのテスト"""
        hand = Hand()
        tiles_ref = hand.tiles

        # 返されるリストは元のリストと異なるインスタンス
        hand.add_tile(Tile(suit="sou", value=1))
        assert len(tiles_ref) == 0  # 元の参照は変更されない
        assert len(hand.tiles) == 1  # 新しく取得したリストは更新されている

    def test_hand_sorting_maintained(self) -> None:
        """常にソート状態が維持されることのテスト"""
        hand = Hand()
        values_to_add = [9, 1, 5, 3, 7, 2, 8, 4, 6]

        for value in values_to_add:
            hand.add_tile(Tile(suit="sou", value=value))

        # 常にソートされていることを確認
        tile_values = [tile.value for tile in hand.tiles]
        assert tile_values == sorted(tile_values)
        assert tile_values == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_hand_clear(self) -> None:
        """手牌のクリアテスト"""
        tiles = [Tile(suit="sou", value=i) for i in range(1, 6)]
        hand = Hand(tiles)

        assert hand.size == 5
        hand.clear()
        assert hand.size == 0
        assert len(hand.tiles) == 0

    def test_hand_get_unique_tiles(self) -> None:
        """ユニークな牌の取得テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)

        unique_tiles = hand.get_unique_tiles()
        assert len(unique_tiles) == 3

        unique_values = sorted([tile.value for tile in unique_tiles])
        assert unique_values == [1, 3, 5]

    def test_hand_get_tile_counts(self) -> None:
        """牌の種類別枚数取得テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)

        tile_counts = hand.get_tile_counts()

        assert tile_counts[Tile(suit="sou", value=1)] == 1
        assert tile_counts[Tile(suit="sou", value=3)] == 3
        assert tile_counts[Tile(suit="sou", value=5)] == 1
        # 存在しない牌は含まれない
        assert Tile(suit="sou", value=2) not in tile_counts

    def test_hand_string_representation(self) -> None:
        """手牌の文字列表現テスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
        ]
        hand = Hand(tiles)

        expected = "1索 3索 3索 5索"
        assert str(hand) == expected

    def test_hand_empty_string_representation(self) -> None:
        """空の手牌の文字列表現テスト"""
        hand = Hand()
        assert str(hand) == "（空）"

    def test_hand_max_size_validation(self) -> None:
        """手牌の最大サイズ検証テスト"""
        hand = Hand()

        # 14枚まで追加可能
        for i in range(14):
            hand.add_tile(Tile(suit="sou", value=(i % 9) + 1))

        assert hand.size == 14

        # 15枚目を追加しようとすると例外
        with pytest.raises(ValueError, match="手牌は最大14枚までです"):
            hand.add_tile(Tile(suit="sou", value=1))

    def test_hand_copy(self) -> None:
        """手牌のコピーテスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
        ]
        original_hand = Hand(tiles)
        copied_hand = original_hand.copy()

        # 内容は同じ
        assert original_hand.tiles == copied_hand.tiles
        assert original_hand.size == copied_hand.size

        # インスタンスは異なる
        assert original_hand is not copied_hand

        # 一方を変更してももう一方に影響しない
        copied_hand.add_tile(Tile(suit="sou", value=7))
        assert original_hand.size == 3
        assert copied_hand.size == 4

    def test_hand_equality(self) -> None:
        """手牌の等価性テスト"""
        tiles1 = [Tile(suit="sou", value=1), Tile(suit="sou", value=3)]
        tiles2 = [Tile(suit="sou", value=3), Tile(suit="sou", value=1)]  # 順序が異なる
        tiles3 = [Tile(suit="sou", value=1), Tile(suit="sou", value=5)]  # 内容が異なる

        hand1 = Hand(tiles1)
        hand2 = Hand(tiles2)
        hand3 = Hand(tiles3)

        assert hand1 == hand2  # 順序に関係なく同じ内容なら等価
        assert hand1 != hand3  # 内容が異なれば非等価
        assert hash(hand1) == hash(hand2)  # 等価なオブジェクトは同じハッシュ
