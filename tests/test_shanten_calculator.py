"""向聴数計算（ShantenCalculator）クラスのテスト"""

import pytest

from mahjong_ai.logic.shanten_calculator import ShantenCalculator
from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


class TestShantenCalculator:
    """向聴数計算クラスのテスト"""

    def setup_method(self) -> None:
        """テストメソッド実行前の初期化"""
        self.calculator = ShantenCalculator()

    def test_calculate_shanten_winning_hand(self) -> None:
        """和了形での向聴数計算テスト（向聴数-1）"""
        # 完成した七対子
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
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == -1, "和了形の向聴数は-1"

    def test_calculate_shanten_tenpai(self) -> None:
        """聴牌での向聴数計算テスト（向聴数0）"""
        # 1枚待ちの聴牌形
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
            # 1索刻子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            # 2索単騎（雀頭待ち）
            Tile(suit="sou", value=2),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == 0, "聴牌形の向聴数は0"

    def test_calculate_shanten_one_shanten(self) -> None:
        """1向聴での向聴数計算テスト"""
        # 1向聴の形
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
            # バラバラ
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=8),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == 1, "1向聴の向聴数は1"

    def test_calculate_shanten_two_shanten(self) -> None:
        """2向聴での向聴数計算テスト"""
        # 2向聴の形
        tiles = [
            # 1-2-3順子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            # 4-5順子の候補
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=5),
            # 7-8順子の候補
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            # 1索対子
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            # バラバラ
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=5),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == 2, "2向聴の向聴数は2"

    def test_calculate_shanten_seven_pairs_tenpai(self) -> None:
        """七対子聴牌での向聴数計算テスト"""
        # 七対子聴牌（6対子+1単騎）
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
            # 7索単騎
            Tile(suit="sou", value=7),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == 0, "七対子聴牌の向聴数は0"

    def test_calculate_shanten_seven_pairs_one_shanten(self) -> None:
        """七対子1向聴での向聴数計算テスト"""
        # 七対子1向聴（5対子+4バラバラ）
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
            # バラバラ
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        assert shanten == 1, "七対子1向聴の向聴数は1"

    def test_calculate_shanten_worst_case(self) -> None:
        """最悪ケースでの向聴数計算テスト"""
        # 全てバラバラ
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_shanten(hand)
        # 最悪でも6向聴程度（完全にバラバラでも何らかの組み合わせは可能）
        assert shanten >= 0, "向聴数は0以上"
        assert shanten <= 6, "向聴数は6以下"

    def test_calculate_shanten_empty_hand(self) -> None:
        """空手牌での向聴数計算テスト"""
        hand = Hand()
        shanten = self.calculator.calculate_shanten(hand)
        # 空手牌の場合、特別な値を返すか、またはエラーになるかを確認
        # 実装方針に応じて調整
        assert shanten >= 0, "空手牌でも向聴数は0以上"

    def test_calculate_shanten_normal_vs_seven_pairs(self) -> None:
        """通常形と七対子の向聴数比較テスト"""
        # 通常形には向かないが七対子には向く形
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=9),
            Tile(suit="sou", value=9),
            # バラバラ
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=6),
        ]
        hand = Hand(tiles)

        # 通常形の向聴数
        normal_shanten = self.calculator.calculate_normal_shanten(hand)

        # 七対子の向聴数
        seven_pairs_shanten = self.calculator.calculate_seven_pairs_shanten(hand)

        # 全体の向聴数（より良い方を選択）
        overall_shanten = self.calculator.calculate_shanten(hand)

        assert overall_shanten <= normal_shanten, "全体向聴数は通常形向聴数以下"
        assert overall_shanten <= seven_pairs_shanten, "全体向聴数は七対子向聴数以下"
        assert overall_shanten == min(normal_shanten, seven_pairs_shanten), "全体向聴数は最小値"

    def test_calculate_normal_shanten(self) -> None:
        """通常形向聴数計算のテスト"""
        # 通常形1向聴
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
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=4),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_normal_shanten(hand)
        assert shanten == 1, "通常形1向聴"

    def test_calculate_seven_pairs_shanten(self) -> None:
        """七対子向聴数計算のテスト"""
        # 七対子2向聴（4対子+5バラバラ）
        tiles = [
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=1),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=2),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=3),
            Tile(suit="sou", value=4),
            Tile(suit="sou", value=4),
            # バラバラ
            Tile(suit="sou", value=5),
            Tile(suit="sou", value=6),
            Tile(suit="sou", value=7),
            Tile(suit="sou", value=8),
            Tile(suit="sou", value=9),
        ]
        hand = Hand(tiles)
        shanten = self.calculator.calculate_seven_pairs_shanten(hand)
        assert shanten == 2, "七対子2向聴"
