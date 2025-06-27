"""和了判定（WinningChecker）クラスのテスト"""

import pytest

from mahjong_ai.logic.winning_checker import WinningChecker
from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


class TestWinningChecker:
    """和了判定クラスのテスト"""

    def setup_method(self) -> None:
        """テストメソッド実行前の初期化"""
        self.checker = WinningChecker()

    def test_is_winning_hand_empty(self) -> None:
        """空の手牌での和了判定テスト"""
        hand = Hand()
        assert not self.checker.is_winning_hand(hand)

    def test_is_winning_hand_wrong_size(self) -> None:
        """14枚でない手牌での和了判定テスト"""
        # 13枚
        tiles = [Tile(suit="sou", value=1) for _ in range(13)]
        hand = Hand(tiles)
        assert not self.checker.is_winning_hand(hand)

        # 15枚は追加不可のため、この場合のテストは省略

    def test_is_winning_hand_simple_complete_sequence(self) -> None:
        """単純な順子完成形での和了判定テスト"""
        # 1-2-3, 4-5-6, 7-8-9, 1-1, 2-2 (14枚)
        tiles = [
            # 1-2-3順子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            # 4-5-6順子
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            # 7-8-9順子
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=9),
            # 1索対子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            # 2索対子（雀頭）
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            # 追加1枚
            Tile(suit="sou", value=3),
        ]
        hand = Hand(tiles)
        assert self.checker.is_winning_hand(hand)

    def test_is_winning_hand_simple_triplet(self) -> None:
        """単純な刻子完成形での和了判定テスト"""
        # 1-1-1, 2-2-2, 3-3-3, 4-4-4, 5-5 (14枚)
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
        assert self.checker.is_winning_hand(hand)

    def test_is_winning_hand_mixed_meld(self) -> None:
        """順子と刻子混合の完成形での和了判定テスト"""
        # 1-1-1, 2-3-4, 5-6-7, 8-8-8, 9-9 (14枚)
        tiles = [
            # 1索刻子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            # 2-3-4順子
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            # 5-6-7順子
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            # 8索刻子
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            # 9索対子（雀頭）
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
        ]
        hand = Hand(tiles)
        assert self.checker.is_winning_hand(hand)

    def test_is_winning_hand_seven_pairs(self) -> None:
        """七対子での和了判定テスト"""
        # 1-1, 2-2, 3-3, 4-4, 5-5, 6-6, 7-7 (14枚)
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=7),
        ]
        hand = Hand(tiles)
        assert self.checker.is_winning_hand(hand)

    def test_is_winning_hand_incomplete_sequences(self) -> None:
        """不完全な順子での和了失敗テスト"""
        # 1-2-4 (完成しない順子)
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=4),  # gap
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
        ]
        hand = Hand(tiles)
        assert not self.checker.is_winning_hand(hand)

    def test_is_winning_hand_incomplete_triplets(self) -> None:
        """不完全な刻子での和了失敗テスト"""
        tiles = [
            # 2枚しかない（刻子にならない）
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=7),
        ]
        hand = Hand(tiles)
        assert not self.checker.is_winning_hand(hand)

    def test_is_winning_hand_no_pair(self) -> None:
        """雀頭がない場合の和了失敗テスト"""
        tiles = [
            # すべて刻子だが雀頭がない
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),  # 対子にならない
        ]
        hand = Hand(tiles)
        assert not self.checker.is_winning_hand(hand)

    def test_is_winning_hand_multiple_pairs_but_not_seven(self) -> None:
        """対子が複数あるが七対子ではない場合のテスト"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=6),
            # 7は1枚のみ（対子にならない）
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
        ]
        hand = Hand(tiles)
        assert not self.checker.is_winning_hand(hand)

    def test_check_seven_pairs_true(self) -> None:
        """七対子判定の正常ケース"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=7),
        ]
        hand = Hand(tiles)
        assert self.checker.check_seven_pairs(hand)

    def test_check_seven_pairs_false_wrong_size(self) -> None:
        """七対子判定の失敗ケース（枚数不正）"""
        tiles = [Tile(suit="sou", value=1) for _ in range(13)]  # 13枚
        hand = Hand(tiles)
        assert not self.checker.check_seven_pairs(hand)

    def test_check_seven_pairs_false_not_pairs(self) -> None:
        """七対子判定の失敗ケース（対子でない）"""
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=6),
            # 1枚のみ
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
        ]
        hand = Hand(tiles)
        assert not self.checker.check_seven_pairs(hand)

    def test_check_normal_winning_form_true(self) -> None:
        """通常の和了形判定の正常ケース"""
        # 1-2-3, 4-5-6, 7-8-9, 1-1-1, 2-2
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
        ]
        hand = Hand(tiles)
        assert self.checker.check_normal_winning_form(hand)

    def test_check_normal_winning_form_false(self) -> None:
        """通常の和了形判定の失敗ケース"""
        # 不完全な形
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=4),  # gap
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
        ]
        hand = Hand(tiles)
        assert not self.checker.check_normal_winning_form(hand)
