"""麻雀の牌を表現するクラス"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Tile:
    """麻雀の牌を表現するイミュータブルクラス

    Phase 1では索子のみをサポートします。
    将来の拡張性を考慮して設計されています。

    Attributes:
        suit: 牌の種類（Phase 1では'sou'のみ）
        value: 牌の数字（1-9）
    """

    suit: str
    value: int

    def __post_init__(self) -> None:
        """初期化後の検証処理"""
        if self.suit != "sou":
            raise ValueError("Phase 1では索子のみサポートしています")

        if not (1 <= self.value <= 9):
            raise ValueError("索子の値は1-9である必要があります")

    @property
    def tile_id(self) -> int:
        """将来の拡張に備えた数値ID

        Returns:
            索子の場合: 0-8 (value - 1)
            将来の拡張: 萬子36-71, 筒子72-107, 字牌108-135
        """
        return self.value - 1

    @property
    def is_terminal(self) -> bool:
        """么九牌（1, 9）かどうかを判定

        Returns:
            么九牌の場合True、そうでなければFalse
        """
        return self.value in (1, 9)

    @property
    def is_middle(self) -> bool:
        """中張牌（2-8）かどうかを判定

        Returns:
            中張牌の場合True、そうでなければFalse
        """
        return 2 <= self.value <= 8

    def __str__(self) -> str:
        """牌の文字列表現

        Returns:
            "1索", "2索", ..., "9索"の形式
        """
        return f"{self.value}索"

    def __lt__(self, other: Any) -> bool:
        """牌の順序比較（小なり）

        Args:
            other: 比較対象

        Returns:
            この牌が小さい場合True

        Raises:
            TypeError: 比較対象がTileでない場合
        """
        if not isinstance(other, Tile):
            raise TypeError("Tileオブジェクト同士でのみ比較可能です")

        # 同じスートの場合は値で比較
        if self.suit == other.suit:
            return self.value < other.value

        # 異なるスートの場合は将来の拡張を考慮
        # Phase 1では索子のみなので、この分岐は使用されない
        suit_order = {"sou": 0, "man": 1, "pin": 2, "honor": 3}
        return suit_order[self.suit] < suit_order[other.suit]

    def __le__(self, other: Any) -> bool:
        """牌の順序比較（小なりイコール）"""
        if not isinstance(other, Tile):
            raise TypeError("Tileオブジェクト同士でのみ比較可能です")
        return self == other or self < other

    def __gt__(self, other: Any) -> bool:
        """牌の順序比較（大なり）"""
        if not isinstance(other, Tile):
            raise TypeError("Tileオブジェクト同士でのみ比較可能です")
        return not self <= other

    def __ge__(self, other: Any) -> bool:
        """牌の順序比較（大なりイコール）"""
        if not isinstance(other, Tile):
            raise TypeError("Tileオブジェクト同士でのみ比較可能です")
        return not self < other
