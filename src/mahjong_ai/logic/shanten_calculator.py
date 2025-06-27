"""向聴数計算ロジック"""

from collections import Counter
from typing import Dict, List

from mahjong_ai.logic.winning_checker import WinningChecker
from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


class ShantenCalculator:
    """向聴数を計算するクラス

    麻雀の手牌の向聴数（あと何枚で聴牌になるか）を計算します。
    Phase 1では索子のみを対象とし、通常形と七対子の向聴数を計算します。
    """

    def __init__(self) -> None:
        """向聴数計算器を初期化"""
        self.winning_checker = WinningChecker()

    def calculate_shanten(self, hand: Hand) -> int:
        """手牌の向聴数を計算

        通常形と七対子の向聴数を計算し、より小さい値を返します。

        Args:
            hand: 向聴数を計算する手牌

        Returns:
            向聴数（-1: 和了, 0: 聴牌, 1以上: n向聴）
        """
        # 和了形の判定
        if hand.size == 14 and self.winning_checker.is_winning_hand(hand):
            return -1

        # 通常形と七対子の向聴数を計算
        normal_shanten = self.calculate_normal_shanten(hand)
        seven_pairs_shanten = self.calculate_seven_pairs_shanten(hand)

        # より小さい方を返す
        return min(normal_shanten, seven_pairs_shanten)

    def calculate_normal_shanten(self, hand: Hand) -> int:
        """通常形（4面子1雀頭）の向聴数を計算

        Args:
            hand: 向聴数を計算する手牌

        Returns:
            通常形の向聴数
        """
        if hand.size == 0:
            return 8  # 空手牌の場合は8向聴相当

        # 各牌の枚数を取得
        tile_counts = hand.get_tile_counts()

        return self._calculate_normal_shanten_recursive(tile_counts)

    def calculate_seven_pairs_shanten(self, hand: Hand) -> int:
        """七対子の向聴数を計算

        Args:
            hand: 向聴数を計算する手牌

        Returns:
            七対子の向聴数
        """
        if hand.size == 0:
            return 6  # 空手牌の場合は6向聴相当

        # 各牌の枚数を取得
        tile_counts = hand.get_tile_counts()

        # 対子の数をカウント
        pairs = 0
        singles = 0

        for count in tile_counts.values():
            if count >= 2:
                pairs += count // 2
            if count % 2 == 1:
                singles += 1

        # 七対子には最大7対子が必要
        pairs = min(pairs, 7)

        # 向聴数 = 6 - 対子数
        shanten = 6 - pairs

        # 13枚の場合の特別処理
        if hand.size == 13:
            if pairs == 6 and singles == 1:
                shanten = 0  # 聴牌
            elif pairs >= 6:
                shanten = 1  # 1向聴

        return max(0, shanten)

    def _calculate_normal_shanten_recursive(self, tile_counts: Dict[Tile, int]) -> int:
        """再帰的に通常形の向聴数を計算

        Args:
            tile_counts: 牌の種類別枚数辞書

        Returns:
            通常形の向聴数
        """
        total_tiles = sum(tile_counts.values())

        if total_tiles == 0:
            return 8

        # 完成した面子数と搭子数を計算
        return self._find_best_shanten(tile_counts, 0, 0, False)

    def _find_best_shanten(self, tile_counts: Dict[Tile, int], melds: int, tatsu: int, has_pair: bool) -> int:
        """最適な向聴数を探索

        Args:
            tile_counts: 牌の種類別枚数辞書
            melds: 完成した面子数
            tatsu: 搭子（候補）数
            has_pair: 雀頭があるかどうか

        Returns:
            向聴数
        """
        # 牌がなくなった場合
        total_tiles = sum(tile_counts.values())
        if total_tiles == 0:
            # 4面子1雀頭の場合
            if melds == 4 and has_pair:
                return -1  # 和了
            elif melds == 4 and not has_pair:
                return 0  # 聴牌
            elif melds == 3 and has_pair:
                return 0  # 聴牌
            else:
                return 8 - melds * 2 - tatsu - (1 if has_pair else 0)

        # 13枚の場合の特別判定
        if total_tiles == 1:
            if melds == 4 and not has_pair:
                return 0  # 単騎待ち聴牌
            else:
                return 8 - melds * 2 - tatsu - (1 if has_pair else 0)

        # 最小の牌から処理
        tiles = sorted(tile_counts.keys())
        if not tiles:
            return 8 - melds * 2 - tatsu - (1 if has_pair else 0)

        first_tile = tiles[0]
        count = tile_counts[first_tile]

        min_shanten = 8

        # 刻子を作る場合
        if count >= 3:
            new_counts = tile_counts.copy()
            new_counts[first_tile] -= 3
            if new_counts[first_tile] == 0:
                del new_counts[first_tile]
            shanten = self._find_best_shanten(new_counts, melds + 1, tatsu, has_pair)
            min_shanten = min(min_shanten, shanten)

        # 対子を作る場合（雀頭がまだない場合）
        if count >= 2 and not has_pair:
            new_counts = tile_counts.copy()
            new_counts[first_tile] -= 2
            if new_counts[first_tile] == 0:
                del new_counts[first_tile]
            shanten = self._find_best_shanten(new_counts, melds, tatsu, True)
            min_shanten = min(min_shanten, shanten)

        # 順子を作る場合
        if first_tile.value <= 7:
            next_tile = Tile(suit="sou", value=first_tile.value + 1)
            next_next_tile = Tile(suit="sou", value=first_tile.value + 2)

            if (
                next_tile in tile_counts
                and next_next_tile in tile_counts
                and tile_counts[next_tile] >= 1
                and tile_counts[next_next_tile] >= 1
            ):

                new_counts = tile_counts.copy()
                new_counts[first_tile] -= 1
                new_counts[next_tile] -= 1
                new_counts[next_next_tile] -= 1

                for tile in [first_tile, next_tile, next_next_tile]:
                    if new_counts[tile] == 0:
                        del new_counts[tile]

                shanten = self._find_best_shanten(new_counts, melds + 1, tatsu, has_pair)
                min_shanten = min(min_shanten, shanten)

        # 搭子（隣り合う2枚）を作る場合
        if first_tile.value <= 8:
            next_tile = Tile(suit="sou", value=first_tile.value + 1)
            if next_tile in tile_counts and tile_counts[next_tile] >= 1:
                new_counts = tile_counts.copy()
                new_counts[first_tile] -= 1
                new_counts[next_tile] -= 1

                for tile in [first_tile, next_tile]:
                    if new_counts[tile] == 0:
                        del new_counts[tile]

                shanten = self._find_best_shanten(new_counts, melds, tatsu + 1, has_pair)
                min_shanten = min(min_shanten, shanten)

        # 搭子（1つ空きの2枚）を作る場合
        if first_tile.value <= 7:
            next_next_tile = Tile(suit="sou", value=first_tile.value + 2)
            if next_next_tile in tile_counts and tile_counts[next_next_tile] >= 1:
                new_counts = tile_counts.copy()
                new_counts[first_tile] -= 1
                new_counts[next_next_tile] -= 1

                for tile in [first_tile, next_next_tile]:
                    if new_counts[tile] == 0:
                        del new_counts[tile]

                shanten = self._find_best_shanten(new_counts, melds, tatsu + 1, has_pair)
                min_shanten = min(min_shanten, shanten)

        # 何も作らずに捨てる場合
        new_counts = tile_counts.copy()
        new_counts[first_tile] -= 1
        if new_counts[first_tile] == 0:
            del new_counts[first_tile]
        shanten = self._find_best_shanten(new_counts, melds, tatsu, has_pair)
        min_shanten = min(min_shanten, shanten)

        return min_shanten
