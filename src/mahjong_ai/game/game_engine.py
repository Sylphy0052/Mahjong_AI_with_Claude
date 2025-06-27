"""ゲームエンジン - 麻雀ゲームの進行を制御"""

from enum import Enum
from typing import Any, Dict, List, Optional

from mahjong_ai.game.wall_tiles import WallTiles
from mahjong_ai.logic.shanten_calculator import ShantenCalculator
from mahjong_ai.logic.winning_checker import WinningChecker
from mahjong_ai.models.hand import Hand
from mahjong_ai.models.tile import Tile
from mahjong_ai.utils.logger import get_logger, log_action, log_error, log_game_state


class GameState(Enum):
    """ゲーム状態を表す列挙型"""

    NOT_STARTED = "not_started"  # ゲーム未開始
    PLAYER_TURN = "player_turn"  # プレイヤーのターン（13枚）
    AFTER_DRAW = "after_draw"  # ツモ後（14枚）
    RIICHI = "riichi"  # リーチ状態
    GAME_OVER = "game_over"  # ゲーム終了


class GameEngine:
    """麻雀ゲームの進行を制御するエンジンクラス

    Phase 1では1人用麻雀として、プレイヤーの行動を管理し、
    和了判定や向聴数計算などのゲームロジックを統合します。
    """

    def __init__(self) -> None:
        """ゲームエンジンを初期化"""
        self.logger = get_logger()
        
        self.current_hand = Hand()
        self.wall = WallTiles()
        self.winning_checker = WinningChecker()
        self.shanten_calculator = ShantenCalculator()

        self.game_state = GameState.NOT_STARTED
        self.turn_count = 0
        self.is_riichi = False
        self.discarded_tiles: List[Tile] = []

        # ゲーム結果
        self.is_winner = False
        self.winning_tile: Optional[Tile] = None
        
        # 最後にツモした牌（ツモ切り用・和了用）
        self.last_drawn_tile: Optional[Tile] = None
        
        # 暗槓した牌のリスト
        self.kan_tiles: List[List[Tile]] = []
        
        self.logger.info("GameEngine初期化完了")
        log_game_state(self)

    def start_game(self) -> None:
        """ゲームを開始

        13枚の初期手牌を配り、ゲーム状態をプレイヤーターンに設定します。

        Raises:
            ValueError: ゲームが既に開始されている場合
        """
        log_action("start_game", "ゲーム開始要求")
        log_game_state(self)
        
        if self.game_state != GameState.NOT_STARTED:
            error = ValueError("ゲームは既に開始されています")
            log_error(error, "start_game")
            raise error

        # 初期手牌を配る（13枚）
        initial_tiles = self.wall.draw_multiple_tiles(13)
        self.current_hand = Hand(initial_tiles)

        # ゲーム状態を更新
        self.game_state = GameState.PLAYER_TURN
        self.turn_count = 1

        print(f"ゲーム開始！ 初期手牌: {self.current_hand}")
        print(f"向聴数: {self.calculate_shanten()}")
        
        log_action("start_game", f"初期手牌配布完了: {self.current_hand}")
        log_game_state(self)

    def draw_tile(self) -> Tile:
        """牌を1枚ツモ

        Returns:
            ツモした牌

        Raises:
            ValueError: ゲームが開始されていない場合、または山牌が空の場合
        """
        log_action("draw_tile", "ツモ要求")
        log_game_state(self)
        
        if self.game_state == GameState.NOT_STARTED:
            error = ValueError("ゲームが開始されていません")
            log_error(error, "draw_tile")
            raise error

        if self.wall.is_empty():
            # 流局処理
            self.game_state = GameState.GAME_OVER
            error = ValueError("山牌が空です（流局）")
            log_error(error, "draw_tile")
            raise error

        # ツモ前の状態をログ
        self.logger.info(f"ツモ前状態: 手牌枚数={self.current_hand.size}, 状態={self.game_state}, リーチ={self.is_riichi}")

        # 牌をツモ
        drawn_tile = self.wall.draw_tile()
        
        try:
            self.current_hand.add_tile(drawn_tile)
            self.logger.info(f"ツモ成功: {drawn_tile}, 手牌枚数={self.current_hand.size}")
        except Exception as e:
            self.logger.error(f"add_tile失敗: {e}")
            log_error(e, f"draw_tile - ツモ牌: {drawn_tile}")
            raise

        # 最後にツモした牌を記録
        self.last_drawn_tile = drawn_tile

        # 状態を更新（リーチ中の場合はリーチ状態を維持）
        old_state = self.game_state
        if not self.is_riichi:
            self.game_state = GameState.AFTER_DRAW
        
        self.logger.info(f"状態変更: {old_state} -> {self.game_state}")

        print(f"ツモ: {drawn_tile}")
        print(f"現在の手牌: {self.current_hand}")

        # 和了可能かチェック（自動和了はしない）
        if self.check_winning_hand():
            print(f"ツモ和了可能！ 和了牌: {drawn_tile}")
            log_action("draw_tile", f"ツモ和了可能: {drawn_tile}")
        
        print(f"向聴数: {self.calculate_shanten()}")
        log_action("draw_tile", f"ツモ完了: {drawn_tile}")

        log_game_state(self)
        return drawn_tile

    def discard_tile(self, tile: Tile, declare_riichi: bool = False) -> None:
        """指定された牌を打牌

        Args:
            tile: 打牌する牌
            declare_riichi: リーチ宣言を行うかどうか

        Raises:
            ValueError: 打牌できる状態でない場合、または指定牌が手牌にない場合
        """
        log_action("discard_tile", f"打牌要求: {tile}, リーチ宣言: {declare_riichi}")
        log_game_state(self)
        
        if self.game_state not in [GameState.AFTER_DRAW, GameState.RIICHI]:
            error = ValueError("打牌できる状態ではありません")
            log_error(error, "discard_tile")
            raise error

        if tile not in self.current_hand.tiles:
            error = ValueError("指定された牌が手牌にありません")
            log_error(error, "discard_tile")
            raise error

        # リーチ宣言のチェック
        if declare_riichi:
            if self.is_riichi:
                error = ValueError("既にリーチしています")
                log_error(error, "discard_tile")
                raise error
            
            # リーチ条件チェック（打牌後に13枚で聴牌状態になるか）
            temp_hand = self.current_hand.copy()
            temp_hand.remove_tile(tile)
            temp_shanten = self.shanten_calculator.calculate_shanten(temp_hand)
            
            if temp_shanten != 0:
                error = ValueError("リーチできません（打牌後に聴牌になりません）")
                log_error(error, "discard_tile")
                raise error

        # リーチ中はツモ切りのみ許可
        if self.is_riichi and self.last_drawn_tile is not None:
            if tile != self.last_drawn_tile:
                error = ValueError("リーチ中はツモ切りしかできません")
                log_error(error, f"discard_tile - 要求牌: {tile}, ツモ牌: {self.last_drawn_tile}")
                raise error

        # 牌を手牌から除去
        self.current_hand.remove_tile(tile)
        self.discarded_tiles.append(tile)

        # リーチ宣言の処理
        if declare_riichi:
            self.is_riichi = True
            self.game_state = GameState.RIICHI
            print("リーチ宣言！")
            log_action("discard_tile", "リーチ宣言実行")
        elif self.game_state != GameState.RIICHI:
            # 通常の打牌後はプレイヤーターンに戻る
            self.game_state = GameState.PLAYER_TURN
        else:
            # リーチ中のツモ切り後もリーチ状態を維持
            self.game_state = GameState.RIICHI

        # ツモ切り完了後はツモ牌をクリア
        self.last_drawn_tile = None
        
        self.turn_count += 1

        print(f"打牌: {tile}")
        print(f"現在の手牌: {self.current_hand}")
        print(f"向聴数: {self.calculate_shanten()}")
        
        log_action("discard_tile", f"打牌完了: {tile}")
        log_game_state(self)

    def check_winning_hand(self) -> bool:
        """現在の手牌が和了形かどうかを判定
        
        暗槓がある場合は、暗槓を除いた手牌で判定します。

        Returns:
            和了形の場合True、そうでなければFalse
        """
        # 暗槓がある場合の特殊判定
        if self.kan_tiles:
            # 暗槓は既に完成した面子として扱う
            # 残りの手牌が1雀頭+面子の形になっていれば和了
            # 暗槓の数 × 3 = 除外する牌数
            required_tiles = 14 - (len(self.kan_tiles) * 4)
            
            # 手牌が必要枚数と一致する場合のみ判定
            if self.current_hand.size == required_tiles:
                # 暗槓を除いた残りの手牌で判定
                # 例: 1暗槓の場合、10枚で3面子1雀頭の判定が必要
                return self._check_winning_with_kan(self.current_hand, len(self.kan_tiles))
        
        # 通常の和了判定
        return self.winning_checker.is_winning_hand(self.current_hand)
    
    def _check_winning_with_kan(self, hand: Hand, kan_count: int) -> bool:
        """暗槓がある場合の和了判定
        
        Args:
            hand: 暗槓を除いた手牌
            kan_count: 暗槓の数
            
        Returns:
            和了形の場合True
        """
        # 暗槓は完成した面子なので、残りの手牌で必要な面子数は減る
        # 例: 1暗槓 → 3面子1雀頭が必要
        #     2暗槓 → 2面子1雀頭が必要
        
        # 簡易実装: 牌数で判定
        # 14枚 - (暗槓数 × 4) = 必要枚数
        expected_size = 14 - (kan_count * 4)
        if hand.size != expected_size:
            return False
        
        # TODO: より詳細な和了判定の実装が必要
        # 現状は手牌枚数のチェックのみで、実際の面子構成は確認していない
        # Phase 1では簡易実装とし、将来的に改善する
        
        # 暫定的に通常の和了判定を流用（完全ではない）
        if expected_size == 2:
            # 2枚の場合は対子のみ
            tiles = hand.tiles
            return len(tiles) == 2 and tiles[0] == tiles[1]
        
        # それ以外は簡易チェック（向聴数で判定）
        return self.shanten_calculator.calculate_shanten(hand) == -1

    def calculate_shanten(self) -> int:
        """現在の手牌の向聴数を計算

        Returns:
            向聴数（-1: 和了, 0: 聴牌, 1以上: n向聴）
        """
        return self.shanten_calculator.calculate_shanten(self.current_hand)


    def get_possible_discards(self) -> List[Tile]:
        """打牌可能な牌のリストを取得

        Returns:
            打牌可能な牌のリスト（重複除去済み）
        """
        if self.game_state != GameState.AFTER_DRAW:
            return []

        # 手牌の牌種類を重複除去して返す
        unique_tiles = []
        seen_tiles = set()

        for tile in self.current_hand.tiles:
            if tile not in seen_tiles:
                unique_tiles.append(tile)
                seen_tiles.add(tile)

        return unique_tiles

    def get_winning_tiles(self) -> List[Tile]:
        """現在聴牌している場合の和了牌を取得

        Returns:
            和了牌のリスト
        """
        # 14枚の状態では聴牌判定はしない（打牌が必要）
        if self.current_hand.size != 13:
            return []
            
        if self.calculate_shanten() != 0:
            return []

        winning_tiles = []

        # 各種類の牌を試して和了判定
        for value in range(1, 10):
            test_tile = Tile(suit="sou", value=value)

            # 山牌にその牌が残っているかチェック
            if self.wall.has_tile(test_tile):
                # 一時的に牌を追加して和了判定
                test_hand = self.current_hand.copy()
                test_hand.add_tile(test_tile)

                if self.winning_checker.is_winning_hand(test_hand):
                    winning_tiles.append(test_tile)

        return winning_tiles

    def get_game_info(self) -> Dict[str, Any]:
        """現在のゲーム状態の情報を取得

        Returns:
            ゲーム状態の辞書
        """
        return {
            "state": self.game_state.value,
            "hand_size": self.current_hand.size,
            "hand_tiles": [str(tile) for tile in self.current_hand.tiles],
            "wall_remaining": self.wall.remaining_count,
            "turn_count": self.turn_count,
            "is_riichi": self.is_riichi,
            "shanten": self.calculate_shanten(),
            "discarded_tiles": [str(tile) for tile in self.discarded_tiles],
            "is_winner": self.is_winner,
            "winning_tile": str(self.winning_tile) if self.winning_tile else None,
        }

    def reset_game(self) -> None:
        """ゲームをリセットして初期状態に戻す"""
        self.current_hand = Hand()
        self.wall.reset()

        self.game_state = GameState.NOT_STARTED
        self.turn_count = 0
        self.is_riichi = False
        self.discarded_tiles.clear()

        self.is_winner = False
        self.winning_tile = None
        self.last_drawn_tile = None
        self.kan_tiles.clear()

        print("ゲームをリセットしました")

    def is_game_over(self) -> bool:
        """ゲームが終了しているかどうかを判定

        Returns:
            ゲーム終了の場合True
        """
        return self.game_state == GameState.GAME_OVER

    def can_draw(self) -> bool:
        """ツモ可能かどうかを判定

        Returns:
            ツモ可能な場合True
        """
        return (
            self.game_state in [GameState.PLAYER_TURN, GameState.RIICHI]
            and not self.wall.is_empty()
            and self.current_hand.size == 13
        )

    def can_discard(self) -> bool:
        """打牌可能かどうかを判定

        Returns:
            打牌可能な場合True
        """
        return self.game_state in [GameState.AFTER_DRAW, GameState.RIICHI] and self.current_hand.size == 14

    def can_win(self) -> bool:
        """ツモ和了可能かどうかを判定
        
        Returns:
            ツモ和了可能な場合True
        """
        return self.check_winning_hand()
    
    def execute_win(self, winning_tile: Tile) -> None:
        """ツモ和了を実行
        
        Args:
            winning_tile: 和了牌
        """
        log_action("execute_win", f"ツモ和了実行: {winning_tile}")
        log_game_state(self)
        
        self.is_winner = True
        self.winning_tile = winning_tile
        self.game_state = GameState.GAME_OVER
        
        print(f"ツモ和了！ 和了牌: {winning_tile}")
        log_action("execute_win", f"ツモ和了完了: {winning_tile}")

    def can_riichi(self) -> bool:
        """リーチ可能かどうかを判定
        
        打牌時にリーチ宣言できる条件をチェックします。
        いずれかの牌を捨てることで13枚で聴牌状態になる場合にTrue。

        Returns:
            リーチ可能な場合True
        """
        if self.is_riichi or self.game_state != GameState.AFTER_DRAW or self.current_hand.size != 14:
            return False
        
        # 各牌を捨てた時に聴牌になるかチェック
        for tile in self.current_hand.tiles:
            temp_hand = self.current_hand.copy()
            temp_hand.remove_tile(tile)
            if self.shanten_calculator.calculate_shanten(temp_hand) == 0:
                return True
        
        return False
    
    def can_discard_for_riichi(self, tile: Tile) -> bool:
        """特定の牌をリーチ宣言して打牌できるかどうかを判定
        
        Args:
            tile: 打牌しようとする牌
            
        Returns:
            その牌を打牌してテンパイになる場合True
        """
        if self.current_hand.size != 14 or tile not in self.current_hand.tiles:
            return False
        
        temp_hand = self.current_hand.copy()
        temp_hand.remove_tile(tile)
        return self.shanten_calculator.calculate_shanten(temp_hand) == 0
    
    def get_riichi_discardable_tiles(self) -> List[Tile]:
        """リーチ宣言時に打牌可能な牌のリストを取得
        
        Returns:
            リーチ宣言して打牌できる牌のリスト
        """
        if not self.can_riichi():
            return []
        
        riichi_tiles = []
        for tile in self.current_hand.tiles:
            if self.can_discard_for_riichi(tile):
                riichi_tiles.append(tile)
        
        return riichi_tiles
    
    def get_kan_possible_tiles(self) -> List[Tile]:
        """暗槓可能な牌のリストを取得
        
        手牌に同じ牌が4枚ある場合、その牌で暗槓が可能。
        
        Returns:
            暗槓可能な牌のリスト（重複なし）
        """
        if self.game_state != GameState.AFTER_DRAW or self.is_riichi:
            return []
        
        kan_tiles = []
        tile_counts = self.current_hand.get_tile_counts()
        
        for tile, count in tile_counts.items():
            if count == 4:
                kan_tiles.append(tile)
        
        return kan_tiles
    
    def can_kan(self) -> bool:
        """暗槓可能かどうかを判定
        
        Returns:
            暗槓可能な場合True
        """
        # リーチ中は暗槓不可
        if self.is_riichi:
            return False
            
        # 嶺上牌がない場合は暗槓不可
        if not self.wall.has_rinshan_tiles():
            return False
            
        return len(self.get_kan_possible_tiles()) > 0
    
    def execute_kan(self, tile: Tile) -> None:
        """暗槓を実行
        
        Args:
            tile: 暗槓する牌
            
        Raises:
            ValueError: 暗槓できない状態、または指定牌で暗槓できない場合
        """
        log_action("execute_kan", f"暗槓要求: {tile}")
        log_game_state(self)
        
        if not self.can_kan():
            error = ValueError("暗槓できる状態ではありません")
            log_error(error, "execute_kan")
            raise error
        
        # 手牌に4枚あるかチェック
        tile_count = self.current_hand.tiles.count(tile)
        if tile_count != 4:
            error = ValueError(f"{tile}が4枚ありません（現在{tile_count}枚）")
            log_error(error, "execute_kan")
            raise error
        
        # 手牌から4枚除去
        for _ in range(4):
            self.current_hand.remove_tile(tile)
        
        # 暗槓リストに追加
        self.kan_tiles.append([tile, tile, tile, tile])
        
        print(f"暗槓: {tile} × 4")
        
        # 嶺上牌をツモ
        rinshan_tile = self.wall.draw_rinshan_tile()
        self.current_hand.add_tile(rinshan_tile)
        
        # 嶺上牌も最後にツモした牌として記録
        self.last_drawn_tile = rinshan_tile
        
        print(f"嶺上ツモ: {rinshan_tile}")
        print(f"現在の手牌: {self.current_hand}")
        
        # 和了可能かチェック（嶺上開花）
        if self.check_winning_hand():
            print(f"嶺上開花可能！ 和了牌: {rinshan_tile}")
            log_action("execute_kan", f"嶺上開花可能: {rinshan_tile}")
        
        # 暗槓後も打牌が必要
        self.game_state = GameState.AFTER_DRAW
        print(f"向聴数: {self.calculate_shanten()}")
        log_action("execute_kan", f"暗槓完了: {tile}")
        
        log_game_state(self)

    def __str__(self) -> str:
        """ゲームエンジンの文字列表現

        Returns:
            現在の状態を表す文字列
        """
        return (
            f"GameEngine(state={self.game_state.value}, "
            f"turn={self.turn_count}, "
            f"hand={self.current_hand.size}枚, "
            f"wall={self.wall.remaining_count}枚)"
        )

    def __repr__(self) -> str:
        """ゲームエンジンの開発者向け表現

        Returns:
            詳細な状態情報
        """
        return self.__str__()
