"""CUIインターフェース - コマンドライン麻雀ゲーム"""

import os
import sys
from typing import List, Optional

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.models.tile import Tile
from mahjong_ai.utils.logger import get_logger, log_action, log_error, log_game_state, log_ui_action


class CUIInterface:
    """コマンドラインユーザーインターフェース

    Phase 1の1人用麻雀をコマンドラインで操作するためのインターフェースです。
    プレイヤーの入力を受け取り、ゲームエンジンを制御してゲームを進行させます。
    """

    def __init__(self) -> None:
        """CUIインターフェースを初期化"""
        self.logger = get_logger()
        self.engine = GameEngine()
        self.running = True
        
        self.logger.info("CUIInterface初期化完了")

    def start(self) -> None:
        """メインゲームループを開始"""
        self.display_welcome_message()

        while self.running:
            try:
                self.main_menu()
            except KeyboardInterrupt:
                self.logger.info("ユーザーによるゲーム終了")
                print("\n\nゲームを終了します...")
                self.running = False
            except Exception as e:
                log_error(e, "メインループ")
                print(f"\nエラーが発生しました: {e}")
                print("続行するには何かキーを押してください...")
                input()

    def main_menu(self) -> None:
        """メインメニューを表示・処理"""
        log_action("main_menu", f"メインメニュー表示: {self.engine.game_state}")
        log_game_state(self.engine)
        
        self.clear_screen()
        self.display_welcome_message()
        self.display_game_state()

        if self.engine.game_state == GameState.NOT_STARTED:
            self.show_start_menu()
        elif self.engine.game_state == GameState.PLAYER_TURN:
            self.show_player_turn_menu()
        elif self.engine.game_state == GameState.AFTER_DRAW:
            self.show_discard_menu()
        elif self.engine.game_state == GameState.RIICHI:
            self.show_riichi_menu()
        elif self.engine.game_state == GameState.GAME_OVER:
            self.show_game_over_menu()

    def show_start_menu(self) -> None:
        """ゲーム開始メニュー"""
        print("\n=== メニュー ===")
        print("1. ゲーム開始")
        print("2. ヘルプ")
        print("3. 終了")

        choice = self.get_menu_choice(3)

        if choice == 1:
            self.process_start_game()
        elif choice == 2:
            self.display_help()
            input("\n続行するには何かキーを押してください...")
        elif choice == 3:
            self.running = False

    def show_player_turn_menu(self) -> None:
        """プレイヤーターンメニュー"""
        print("\n=== プレイヤーターン ===")
        print("1. ツモ")
        print("2. ヘルプ")
        print("3. ゲームリセット")

        choice = self.get_menu_choice(3)

        if choice == 1:
            self.process_draw_tile()
        elif choice == 2:
            self.display_help()
            input("\n続行するには何かキーを押してください...")
        elif choice == 3:
            self.engine.reset_game()

    def show_discard_menu(self) -> None:
        """打牌メニュー"""
        print("\n=== 打牌選択 ===")
        
        # リーチ中のツモ切り制限を表示
        if self.engine.is_riichi and self.engine.last_drawn_tile is not None:
            print(f"リーチ中です。ツモ切りのみ可能です: {self.engine.last_drawn_tile}")
            # ツモ牌の番号を特定
            drawn_tile_index = None
            for i, tile in enumerate(self.engine.current_hand.tiles):
                if tile == self.engine.last_drawn_tile:
                    drawn_tile_index = i + 1  # 1-based index
                    break
            if drawn_tile_index:
                print(f"自動選択: [{drawn_tile_index}] {self.engine.last_drawn_tile}")
                # 自動でツモ切り実行
                self.engine.discard_tile(self.engine.last_drawn_tile)
                input("\n続行するには何かキーを押してください...")
                return
        
        # ツモ和了可能かチェック
        actions = []
        if self.engine.can_win():
            actions.append("ツモ和了")
        actions.append("打牌する")
        if self.engine.can_kan():
            actions.append("暗槓する")
        
        if len(actions) > 1:
            print("\n*** アクション選択 ***")
            for i, action in enumerate(actions, 1):
                print(f"{i}. {action}")
            
            choice = self.get_menu_choice(len(actions))
            
            if actions[choice - 1] == "ツモ和了":
                self.process_win()
                return
            elif actions[choice - 1] == "暗槓する":
                self.process_kan()
                return
        
        
        self.display_numbered_hand()
        
        # リーチ可能かどうかを表示
        if self.engine.can_riichi():
            print("\n*** リーチ可能です！ ***")
            riichi_tiles = self.engine.get_riichi_discardable_tiles()
            if riichi_tiles:
                print("リーチ宣言可能な牌:")
                for i, tile in enumerate(self.engine.current_hand.tiles):
                    if tile in riichi_tiles:
                        print(f"  [{i+1}] {tile} ← リーチ可能")
                    else:
                        print(f"  [{i+1}] {tile}")
            print("打牌する牌の番号を選択してください（1-14）:")
            print("リーチ宣言したい場合は番号の後に 'r' を付けてください（例: 5r）")
        else:
            print("\n打牌する牌の番号を選択してください（1-14）:")

        self.process_discard_tile()

    def show_riichi_menu(self) -> None:
        """リーチ状態メニュー"""
        print("\n=== リーチ中 ===")
        
        # 打牌可能な場合は打牌メニューを表示
        if self.engine.can_discard():
            self.show_discard_menu()
            return
        
        # ツモ可能な場合のみツモオプションを表示
        if self.engine.can_draw():
            print("1. ツモ")
            print("2. ヘルプ")
            print("3. ゲームリセット")
            max_choice = 3
        else:
            print("1. ヘルプ")
            print("2. ゲームリセット")
            max_choice = 2

        choice = self.get_menu_choice(max_choice)

        if choice == 1 and self.engine.can_draw():
            self.process_draw_tile()
        elif (choice == 1 and not self.engine.can_draw()) or (choice == 2 and self.engine.can_draw()):
            self.display_help()
            input("\n続行するには何かキーを押してください...")
        elif (choice == 2 and not self.engine.can_draw()) or (choice == 3 and self.engine.can_draw()):
            self.engine.reset_game()

    def process_kan(self) -> None:
        """暗槓処理"""
        log_action("process_kan", "暗槓処理開始")
        log_game_state(self.engine)
        
        # 暗槓可能な牌を取得
        kan_tiles = self.engine.get_kan_possible_tiles()
        
        if not kan_tiles:
            print("暗槓できる牌がありません")
            input("\n続行するには何かキーを押してください...")
            return
        
        print("\n=== 暗槓可能な牌 ===")
        for i, tile in enumerate(kan_tiles, 1):
            print(f"{i}. {tile} × 4")
        print(f"{len(kan_tiles) + 1}. キャンセル")
        
        # 暗槓する牌を選択
        max_choice = len(kan_tiles) + 1
        while True:
            try:
                choice = int(input(f"\n暗槓する牌を選択してください (1-{max_choice}): "))
                if choice == max_choice:
                    # キャンセル
                    return
                if 1 <= choice < max_choice:
                    selected_tile = kan_tiles[choice - 1]
                    break
                else:
                    print(f"1から{max_choice}の数字を入力してください")
            except ValueError:
                print("数字を入力してください")
        
        try:
            # 暗槓を実行
            self.engine.execute_kan(selected_tile)
            
            # 嶺上開花の場合
            if self.engine.is_game_over() and self.engine.is_winner:
                self.display_winning_message(self.engine.winning_tile)
            
            input("\n続行するには何かキーを押してください...")
            
        except ValueError as e:
            log_error(e, "process_kan")
            print(f"エラー: {e}")
            input("\n続行するには何かキーを押してください...")

    def process_win(self) -> None:
        """ツモ和了処理"""
        log_action("process_win", "ツモ和了処理開始")
        log_game_state(self.engine)
        
        if not self.engine.can_win():
            print("和了できません")
            input("\n続行するには何かキーを押してください...")
            return
        
        try:
            # 最後にツモした牌を和了牌として実行
            winning_tile = self.engine.last_drawn_tile
            if not winning_tile:
                print("ツモ牌が特定できません")
                return
            
            self.engine.execute_win(winning_tile)
            
            self.display_winning_message(winning_tile)
            input("\n続行するには何かキーを押してください...")
            
        except Exception as e:
            log_error(e, "process_win")
            print(f"エラー: {e}")
            input("\n続行するには何かキーを押してください...")

    def show_game_over_menu(self) -> None:
        """ゲーム終了メニュー"""
        self.display_game_result()

        print("\n=== ゲーム終了 ===")
        print("1. 新しいゲーム")
        print("2. 終了")

        choice = self.get_menu_choice(2)

        if choice == 1:
            self.engine.reset_game()
        elif choice == 2:
            self.running = False

    def process_start_game(self) -> None:
        """ゲーム開始処理"""
        print("\nゲームを開始します...")
        self.engine.start_game()
        input("\n続行するには何かキーを押してください...")

    def process_draw_tile(self) -> Tile:
        """ツモ処理"""
        log_action("process_draw_tile", "ツモ処理開始")
        log_game_state(self.engine)
        
        if not self.engine.can_draw():
            self.logger.warning(f"ツモ不可: can_draw()=False")
            print("ツモできません")
            input("\n続行するには何かキーを押してください...")
            return

        try:
            self.logger.info("engine.draw_tile()呼び出し前")
            drawn_tile = self.engine.draw_tile()
            self.logger.info(f"engine.draw_tile()呼び出し後: {drawn_tile}")

            if self.engine.is_game_over():
                if self.engine.is_winner:
                    self.display_winning_message(drawn_tile)
                else:
                    print("流局しました")

            input("\n続行するには何かキーを押してください...")
            return drawn_tile

        except ValueError as e:
            log_error(e, "process_draw_tile")
            print(f"エラー: {e}")
            input("\n続行するには何かキーを押してください...")

    def process_discard_tile(self) -> None:
        """打牌処理"""
        if not self.engine.can_discard():
            print("打牌できません")
            input("\n続行するには何かキーを押してください...")
            return

        while True:
            try:
                choice_result = self.get_discard_choice()
                if choice_result is None:
                    return

                choice, declare_riichi = choice_result

                # 1-based index を 0-based に変換
                tile_index = choice - 1
                hand_tiles = self.engine.current_hand.tiles

                if 0 <= tile_index < len(hand_tiles):
                    discard_tile = hand_tiles[tile_index]
                    
                    # リーチ中のツモ切り制限チェック
                    if self.engine.is_riichi and self.engine.last_drawn_tile is not None:
                        if discard_tile != self.engine.last_drawn_tile:
                            print(f"エラー: リーチ中はツモ切りのみ可能です（ツモ牌: {self.engine.last_drawn_tile}）")
                            continue
                    
                    # リーチ宣言のチェック
                    if declare_riichi:
                        if not self.engine.can_riichi():
                            print("エラー: リーチできません")
                            continue
                        if not self.engine.can_discard_for_riichi(discard_tile):
                            print(f"エラー: {discard_tile}を打牌するとテンパイになりません")
                            continue
                        print(f"リーチ宣言して {discard_tile} を打牌します")
                    
                    self.engine.discard_tile(discard_tile, declare_riichi)
                    
                    if declare_riichi:
                        print(f"\n{discard_tile}を打牌してリーチ宣言しました！")
                    else:
                        print(f"\n{discard_tile}を打牌しました")
                    break
                else:
                    print("無効な選択です")

            except ValueError as e:
                log_error(e, "process_discard_tile")
                print(f"エラー: {e}")

        input("\n続行するには何かキーを押してください...")


    def display_welcome_message(self) -> None:
        """ウェルカムメッセージ表示"""
        print("=" * 50)
        print("    麻雀AI Phase 1 - CUI版1人用麻雀（索子のみ）")
        print("=" * 50)

    def display_game_state(self) -> None:
        """ゲーム状態表示"""
        if self.engine.game_state == GameState.NOT_STARTED:
            print("\nゲーム状態: 未開始")
            return

        print(f"\nゲーム状態: {self.get_state_description()}")
        print(f"ターン数: {self.engine.turn_count}")
        print(f"山牌残り: {self.engine.wall.remaining_count}枚")

        if self.engine.is_riichi:
            print("リーチ中！")

        self.display_hand()

        shanten = self.engine.calculate_shanten()
        if shanten == -1:
            print("和了形です！")
        elif shanten == 0:
            # 13枚の状態でのみ聴牌表示
            if self.engine.current_hand.size == 13:
                print("聴牌中です！")
                winning_tiles = self.engine.get_winning_tiles()
                if winning_tiles:
                    print(f"待ち牌: {self.format_tile_list(winning_tiles)}")
            else:
                print(f"向聴数: {shanten}")
        else:
            print(f"向聴数: {shanten}")

        if self.engine.discarded_tiles:
            print(f"捨て牌: {self.format_tile_list(self.engine.discarded_tiles)}")
        
        if self.engine.kan_tiles:
            print(f"暗槓: {self.format_kan_tiles()}")

    def display_hand(self) -> None:
        """手牌表示"""
        if self.engine.current_hand.size == 0:
            print("手牌: なし")
        else:
            print(f"手牌({self.engine.current_hand.size}枚): {self.engine.current_hand}")

    def display_numbered_hand(self) -> None:
        """番号付き手牌表示"""
        print(f"\n手牌({self.engine.current_hand.size}枚):")
        tiles = self.engine.current_hand.tiles

        for i, tile in enumerate(tiles, 1):
            print(f"{i:2d}: {tile}")

    def display_winning_message(self, winning_tile: Tile) -> None:
        """和了メッセージ表示"""
        print("\n" + "=" * 30)
        print("    🎉 和了！おめでとうございます！ 🎉")
        print("=" * 30)
        print(f"和了牌: {winning_tile}")
        print(f"最終手牌: {self.engine.current_hand}")

    def display_game_result(self) -> None:
        """ゲーム結果表示"""
        if self.engine.is_winner:
            self.display_winning_message(self.engine.winning_tile)
        else:
            print("\n" + "=" * 20)
            print("    流局")
            print("=" * 20)
            print(f"最終手牌: {self.engine.current_hand}")
            shanten = self.engine.calculate_shanten()
            print(f"最終向聴数: {shanten}")

    def display_help(self) -> None:
        """ヘルプ表示"""
        print("\n" + "=" * 40)
        print("    ヘルプ - 麻雀AI Phase 1")
        print("=" * 40)
        print("\n【ゲームの目的】")
        print("・索子のみを使用した1人用麻雀です")
        print("・14枚で和了形を作ることが目標です")
        print("・和了形: 4面子1雀頭 または 七対子")
        print("\n【基本操作】")
        print("・ツモ: 山牌から1枚引く（13枚→14枚）")
        print("・打牌: 14枚から1枚捨てる（14枚→13枚）")
        print("・リーチ: 聴牌時に宣言可能")
        print("\n【向聴数】")
        print("・-1: 和了形")
        print("・ 0: 聴牌（あと1枚で和了）")
        print("・ 1以上: n向聴（あとn+1枚で和了）")

    def get_menu_choice(self, max_choice: int) -> int:
        """メニュー選択取得"""
        while True:
            try:
                choice = int(input(f"\n選択してください (1-{max_choice}): "))
                if 1 <= choice <= max_choice:
                    log_ui_action("menu_choice", choice, max_choice)
                    return choice
                else:
                    print(f"1から{max_choice}の数字を入力してください")
            except ValueError:
                print("数字を入力してください")

    def get_discard_choice(self) -> Optional[tuple]:
        """打牌選択取得
        
        Returns:
            (tile_index, declare_riichi) のタプル、またはNone
        """
        while True:
            try:
                choice_str = input("打牌する牌の番号 (1-14): ").strip().lower()

                if choice_str in ["q", "quit", "cancel"]:
                    return None

                # リーチ宣言チェック（'r'が末尾にある場合）
                declare_riichi = choice_str.endswith('r')
                if declare_riichi:
                    choice_str = choice_str[:-1]  # 'r'を除去

                choice = int(choice_str)
                if self.validate_discard_choice(choice):
                    return (choice, declare_riichi)
                else:
                    print("1から14の数字を入力してください")

            except ValueError:
                print("数字を入力してください（qでキャンセル、リーチは番号+r）")

    def validate_discard_choice(self, choice: int) -> bool:
        """打牌選択の妥当性検証"""
        return 1 <= choice <= self.engine.current_hand.size

    def format_tile_list(self, tiles: List[Tile]) -> str:
        """牌リストの整形"""
        return " ".join(str(tile) for tile in tiles)
    
    def format_kan_tiles(self) -> str:
        """暗槓牌リストの整形"""
        kan_groups = []
        for kan_set in self.engine.kan_tiles:
            # 同じ牌4枚なので最初の1枚を取得
            tile = kan_set[0]
            kan_groups.append(f"{tile}×4")
        return " ".join(kan_groups)

    def get_numbered_tile_display(self) -> str:
        """番号付き牌表示の取得"""
        tiles = self.engine.current_hand.tiles
        return "\n".join(f"{i+1:2d}: {tile}" for i, tile in enumerate(tiles))

    def get_state_description(self) -> str:
        """状態説明の取得"""
        state_map = {
            GameState.NOT_STARTED: "未開始",
            GameState.PLAYER_TURN: "プレイヤーターン",
            GameState.AFTER_DRAW: "ツモ後",
            GameState.RIICHI: "リーチ中",
            GameState.GAME_OVER: "ゲーム終了",
        }
        return state_map.get(self.engine.game_state, "不明")

    def clear_screen(self) -> None:
        """画面クリア"""
        os.system("cls" if os.name == "nt" else "clear")

    def get_command_input(self) -> str:
        """コマンド入力取得"""
        return input("コマンド: ").strip().lower()

    def display_game_over_message(self, is_winner: bool, reason: str = "") -> None:
        """ゲーム終了メッセージ表示"""
        print("\n" + "=" * 30)
        if is_winner:
            print("    ゲーム終了 - 勝利！")
        else:
            print("    ゲーム終了")
        if reason:
            print(f"    理由: {reason}")
        print("=" * 30)

    def display_possible_actions(self) -> None:
        """可能なアクション表示"""
        print("\n利用可能なアクション:")

        if self.engine.can_draw():
            print("・ツモ")

        if self.engine.can_discard():
            print("・打牌")

        if self.engine.can_riichi():
            print("・リーチ宣言")

    def run_game(self) -> None:
        """ゲーム実行（外部から呼び出し用）"""
        try:
            self.start()
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
        finally:
            print("ゲームを終了しました。ありがとうございました！")


def main() -> None:
    """メイン関数"""
    interface = CUIInterface()
    interface.run_game()


if __name__ == "__main__":
    main()
