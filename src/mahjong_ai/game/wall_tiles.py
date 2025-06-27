"""山牌管理システム"""

import random
from typing import List, Optional

from mahjong_ai.models.tile import Tile


class WallTiles:
    """山牌を管理するクラス

    麻雀の山牌（残りの牌）を管理し、牌の抽選機能を提供します。
    Phase 1では索子のみをサポートし、各種類6枚ずつ計54枚を管理します。
    """

    def __init__(self) -> None:
        """山牌を初期化"""
        self._tiles: List[Tile] = []
        self._rinshan_tiles: List[Tile] = []  # 嶺上牌
        self.reset()

    @property
    def remaining_tiles(self) -> List[Tile]:
        """残り牌のリスト（読み取り専用）

        Returns:
            残り牌のリストのコピー
        """
        return self._tiles.copy()

    @property
    def remaining_count(self) -> int:
        """残り牌数

        Returns:
            現在の残り牌数
        """
        return len(self._tiles)
    
    @property
    def rinshan_count(self) -> int:
        """嶺上牌の残り枚数
        
        Returns:
            嶺上牌の残り枚数
        """
        return len(self._rinshan_tiles)

    def reset(self) -> None:
        """山牌をリセット（初期状態に戻す）"""
        self._tiles.clear()
        self._rinshan_tiles.clear()

        # 索子1-9を各6枚ずつ作成
        all_tiles = []
        for value in range(1, 10):
            for _ in range(6):
                all_tiles.append(Tile(suit="sou", value=value))

        # シャッフル
        random.shuffle(all_tiles)
        
        # 嶺上牌として4枚を分離
        self._rinshan_tiles = all_tiles[:4]
        self._tiles = all_tiles[4:]

    def draw_tile(self) -> Tile:
        """牌を1枚抽選

        Returns:
            抽選された牌

        Raises:
            ValueError: 山牌が空の場合
        """
        if not self._tiles:
            raise ValueError("山牌が空です")

        # 最後の牌を取得（効率的）
        return self._tiles.pop()

    def peek_next_tile(self) -> Tile:
        """次に抽選される牌を確認（実際には抽選しない）

        Returns:
            次に抽選される牌

        Raises:
            ValueError: 山牌が空の場合
        """
        if not self._tiles:
            raise ValueError("山牌が空です")

        # 最後の牌を確認
        return self._tiles[-1]

    def has_tile(self, tile: Tile) -> bool:
        """指定された牌が山牌に存在するかチェック

        Args:
            tile: チェックする牌

        Returns:
            存在する場合True、そうでなければFalse
        """
        return tile in self._tiles

    def count_tile(self, tile: Tile) -> int:
        """指定された牌の残り枚数をカウント

        Args:
            tile: カウントする牌

        Returns:
            指定された牌の残り枚数
        """
        return self._tiles.count(tile)

    def draw_specific_tile(self, tile: Tile) -> Tile:
        """特定の牌を抽選（デバッグ用）

        通常のゲームでは使用しませんが、テストやデバッグ時に便利です。

        Args:
            tile: 抽選したい牌

        Returns:
            抽選された牌

        Raises:
            ValueError: 指定された牌が山牌に存在しない場合
        """
        if tile not in self._tiles:
            raise ValueError(f"指定された牌{tile}が山牌に存在しません")

        # 指定された牌を除去
        self._tiles.remove(tile)
        return tile

    def get_tile_distribution(self) -> dict[Tile, int]:
        """現在の山牌の牌分布を取得

        Returns:
            牌をキー、枚数を値とする辞書
        """
        distribution = {}
        for value in range(1, 10):
            tile = Tile(suit="sou", value=value)
            distribution[tile] = self.count_tile(tile)
        return distribution

    def is_empty(self) -> bool:
        """山牌が空かどうかを判定

        Returns:
            空の場合True、そうでなければFalse
        """
        return len(self._tiles) == 0

    def draw_multiple_tiles(self, count: int) -> List[Tile]:
        """複数の牌を一度に抽選

        Args:
            count: 抽選する牌数

        Returns:
            抽選された牌のリスト

        Raises:
            ValueError: 山牌の残り枚数が不足している場合
        """
        if count > self.remaining_count:
            raise ValueError(f"山牌の残り枚数（{self.remaining_count}）が不足しています（要求: {count}）")

        drawn_tiles = []
        for _ in range(count):
            drawn_tiles.append(self.draw_tile())

        return drawn_tiles
    
    def draw_rinshan_tile(self) -> Tile:
        """嶺上牌を1枚抽選
        
        Returns:
            抽選された嶺上牌
            
        Raises:
            ValueError: 嶺上牌が空の場合
        """
        if not self._rinshan_tiles:
            raise ValueError("嶺上牌が空です")
        
        return self._rinshan_tiles.pop()
    
    def has_rinshan_tiles(self) -> bool:
        """嶺上牌が残っているかチェック
        
        Returns:
            嶺上牌が残っている場合True
        """
        return len(self._rinshan_tiles) > 0

    def __str__(self) -> str:
        """山牌の文字列表現

        Returns:
            残り枚数と分布の概要
        """
        if self.is_empty():
            return "山牌: 空"

        distribution = self.get_tile_distribution()
        dist_str = ", ".join(f"{tile.value}索:{count}枚" for tile, count in sorted(distribution.items()) if count > 0)

        return f"山牌: {self.remaining_count}枚 ({dist_str})"

    def __repr__(self) -> str:
        """山牌の開発者向け表現

        Returns:
            WallTiles(remaining=X)の形式
        """
        return f"WallTiles(remaining={self.remaining_count})"
