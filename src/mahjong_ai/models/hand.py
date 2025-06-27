"""手牌を管理するクラス"""

from collections import Counter
from typing import Dict, List, Optional

from mahjong_ai.models.tile import Tile


class Hand:
    """手牌を管理するクラス

    麻雀の手牌を表現し、牌の追加・削除・検索機能を提供します。
    常にソート状態を維持し、最大14枚まで保持できます。

    Attributes:
        _tiles: 手牌の牌リスト（内部管理用、常にソート済み）
    """

    MAX_SIZE = 14

    def __init__(self, tiles: Optional[List[Tile]] = None) -> None:
        """手牌を初期化

        Args:
            tiles: 初期牌のリスト（Noneの場合は空で初期化）
        """
        self._tiles: List[Tile] = []
        if tiles:
            for tile in tiles:
                self.add_tile(tile)

    @property
    def tiles(self) -> List[Tile]:
        """手牌の牌リストの読み取り専用ビュー

        Returns:
            ソート済み牌リストのコピー
        """
        return self._tiles.copy()

    @property
    def size(self) -> int:
        """手牌の牌数

        Returns:
            現在の手牌の牌数
        """
        return len(self._tiles)

    def add_tile(self, tile: Tile) -> None:
        """牌を追加

        追加後は自動的にソートされます。

        Args:
            tile: 追加する牌

        Raises:
            ValueError: 手牌が最大サイズ（14枚）に達している場合
        """
        if self.size >= self.MAX_SIZE:
            raise ValueError("手牌は最大14枚までです")

        self._tiles.append(tile)
        self._tiles.sort()

    def remove_tile(self, tile: Tile) -> None:
        """牌を除去

        指定された牌を1枚除去します。同じ牌が複数ある場合は最初の1枚のみ。

        Args:
            tile: 除去する牌

        Raises:
            ValueError: 指定された牌が手牌に存在しない場合
        """
        try:
            self._tiles.remove(tile)
        except ValueError:
            raise ValueError("指定された牌が手牌に存在しません")

    def has_tile(self, tile: Tile) -> bool:
        """指定された牌が手牌に存在するかチェック

        Args:
            tile: チェックする牌

        Returns:
            存在する場合True、そうでなければFalse
        """
        return tile in self._tiles

    def count_tile(self, tile: Tile) -> int:
        """指定された牌の枚数をカウント

        Args:
            tile: カウントする牌

        Returns:
            指定された牌の枚数
        """
        return self._tiles.count(tile)

    def clear(self) -> None:
        """手牌をクリア（全ての牌を除去）"""
        self._tiles.clear()

    def get_unique_tiles(self) -> List[Tile]:
        """ユニークな牌のリストを取得

        Returns:
            重複を除いた牌のリスト（ソート済み）
        """
        unique_tiles = list(set(self._tiles))
        unique_tiles.sort()
        return unique_tiles

    def get_tile_counts(self) -> Dict[Tile, int]:
        """牌の種類別枚数を取得

        Returns:
            牌をキー、枚数を値とする辞書
        """
        return dict(Counter(self._tiles))

    def copy(self) -> "Hand":
        """手牌のコピーを作成

        Returns:
            この手牌と同じ内容の新しいHandインスタンス
        """
        return Hand(self._tiles)

    def __str__(self) -> str:
        """手牌の文字列表現

        Returns:
            牌を空白区切りで並べた文字列（空の場合は「（空）」）
        """
        if not self._tiles:
            return "（空）"

        return " ".join(str(tile) for tile in self._tiles)

    def __repr__(self) -> str:
        """手牌の開発者向け表現

        Returns:
            Hand(tiles=[...])の形式
        """
        return f"Hand(tiles={self._tiles!r})"

    def __eq__(self, other: object) -> bool:
        """手牌の等価性チェック

        Args:
            other: 比較対象

        Returns:
            同じ牌の組み合わせの場合True
        """
        if not isinstance(other, Hand):
            return False

        # ソート済みなので直接比較可能
        return self._tiles == other._tiles

    def __hash__(self) -> int:
        """手牌のハッシュ値

        Returns:
            牌の組み合わせに基づくハッシュ値
        """
        return hash(tuple(self._tiles))
