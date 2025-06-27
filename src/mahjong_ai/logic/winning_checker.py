"""和了判定ロジック"""

from collections import Counter
from typing import Dict, List

from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile


class WinningChecker:
    """和了判定を行うクラス

    麻雀の手牌が和了形（あがり形）かどうかを判定します。
    Phase 1では索子のみを対象とし、通常の和了形と七対子を判定します。
    """

    def is_winning_hand(self, hand: Hand) -> bool:
        """手牌が和了形かどうかを判定

        Args:
            hand: 判定対象の手牌

        Returns:
            和了形の場合True、そうでなければFalse
        """
        # 14枚でなければ和了不可
        if hand.size != 14:
            return False

        # 七対子の判定
        if self.check_seven_pairs(hand):
            return True

        # 通常の和了形の判定
        return self.check_normal_winning_form(hand)

    def check_seven_pairs(self, hand: Hand) -> bool:
        """七対子かどうかを判定

        Args:
            hand: 判定対象の手牌

        Returns:
            七対子の場合True、そうでなければFalse
        """
        # 14枚でなければ七対子不可
        if hand.size != 14:
            return False

        # 各牌の枚数を取得
        tile_counts = hand.get_tile_counts()

        # 7種類の牌があり、すべて2枚ずつであることを確認
        if len(tile_counts) != 7:
            return False

        return all(count == 2 for count in tile_counts.values())

    def check_normal_winning_form(self, hand: Hand) -> bool:
        """通常の和了形（4面子1雀頭）かどうかを判定

        Args:
            hand: 判定対象の手牌

        Returns:
            通常の和了形の場合True、そうでなければFalse
        """
        # 14枚でなければ和了不可
        if hand.size != 14:
            return False

        # 各牌の枚数を取得
        tile_counts = hand.get_tile_counts()

        # 再帰的に面子を除去して判定
        return self._check_winning_form_recursive(tile_counts)

    def _check_winning_form_recursive(self, tile_counts: Dict[Tile, int]) -> bool:
        """再帰的に面子を除去して和了形を判定

        Args:
            tile_counts: 牌の種類別枚数辞書

        Returns:
            和了形の場合True、そうでなければFalse
        """
        # 牌がなくなったら成功
        total_tiles = sum(tile_counts.values())
        if total_tiles == 0:
            return True

        # 雀頭（対子）が残っている場合
        if total_tiles == 2:
            return any(count == 2 for count in tile_counts.values())

        # 雀頭を選んでから面子を除去
        for tile, count in tile_counts.items():
            if count >= 2:
                # 雀頭として使用
                new_counts = tile_counts.copy()
                new_counts[tile] -= 2
                if new_counts[tile] == 0:
                    del new_counts[tile]

                # 残りの牌で面子を作れるかチェック
                if self._check_melds_only(new_counts):
                    return True

        return False

    def _check_melds_only(self, tile_counts: Dict[Tile, int]) -> bool:
        """面子のみで構成できるかを判定（雀頭なし）

        Args:
            tile_counts: 牌の種類別枚数辞書

        Returns:
            面子のみで構成できる場合True、そうでなければFalse
        """
        # 牌がなくなったら成功
        if not tile_counts or sum(tile_counts.values()) == 0:
            return True

        # 残り牌数が3の倍数でなければ失敗
        if sum(tile_counts.values()) % 3 != 0:
            return False

        # 最小の牌から処理
        tiles = sorted(tile_counts.keys())
        first_tile = tiles[0]
        count = tile_counts[first_tile]

        # 刻子を作る場合
        if count >= 3:
            new_counts = tile_counts.copy()
            new_counts[first_tile] -= 3
            if new_counts[first_tile] == 0:
                del new_counts[first_tile]

            if self._check_melds_only(new_counts):
                return True

        # 順子を作る場合（value+1, value+2の牌が必要）
        if first_tile.value <= 7:  # 1-7索のみ順子の先頭になれる
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

                # カウントが0になった牌を削除
                for tile in [first_tile, next_tile, next_next_tile]:
                    if new_counts[tile] == 0:
                        del new_counts[tile]

                if self._check_melds_only(new_counts):
                    return True

        return False
