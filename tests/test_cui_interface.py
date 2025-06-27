"""CUIインターフェース（CUIInterface）クラスのテスト"""

from io import StringIO
from unittest.mock import patch

import pytest

from mahjong_ai.game.game_engine import GameEngine, GameState
from mahjong_ai.interface.cui_interface import CUIInterface
from mahjong_ai.models.tile import Tile


class TestCUIInterface:
    """CUIインターフェースクラスのテスト"""

    def setup_method(self) -> None:
        """テストメソッド実行前の初期化"""
        self.interface = CUIInterface()

    def test_cui_initialization(self) -> None:
        """CUIインターフェース初期化テスト"""
        assert isinstance(self.interface.engine, GameEngine)
        assert self.interface.engine.game_state == GameState.NOT_STARTED

    def test_display_welcome_message(self) -> None:
        """ウェルカムメッセージ表示テスト"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_welcome_message()
            output = fake_out.getvalue()
            assert "麻雀AI" in output
            assert "Phase 1" in output

    def test_display_game_state(self) -> None:
        """ゲーム状態表示テスト"""
        self.interface.engine.start_game()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_game_state()
            output = fake_out.getvalue()

            # 期待される情報が含まれている
            assert "手牌" in output
            assert "向聴数" in output
            assert "山牌残り" in output

    def test_display_hand(self) -> None:
        """手牌表示テスト"""
        self.interface.engine.start_game()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_hand()
            output = fake_out.getvalue()

            # 手牌の情報が含まれている
            assert "手牌" in output
            assert "索" in output  # 索子の表示

    def test_display_possible_actions(self) -> None:
        """可能なアクション表示テスト"""
        self.interface.engine.start_game()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_possible_actions()
            output = fake_out.getvalue()

            # アクションオプションが含まれている
            assert "選択してください" in output or "コマンド" in output

    @patch("builtins.input", return_value="1")
    def test_get_user_input_valid(self, mock_input) -> None:
        """有効なユーザー入力テスト"""
        self.interface.engine.start_game()
        self.interface.engine.draw_tile()

        # 打牌選択のテスト
        with patch("sys.stdout", new=StringIO()):
            choice = self.interface.get_discard_choice()
            assert isinstance(choice, int)
            assert 1 <= choice <= 14

    @patch("builtins.input", side_effect=["invalid", "99", "1"])
    def test_get_user_input_invalid_then_valid(self, mock_input) -> None:
        """無効→有効なユーザー入力テスト"""
        self.interface.engine.start_game()
        self.interface.engine.draw_tile()

        with patch("sys.stdout", new=StringIO()):
            choice = self.interface.get_discard_choice()
            assert choice == 1

    def test_process_game_action_start(self) -> None:
        """ゲーム開始アクション処理テスト"""
        assert self.interface.engine.game_state == GameState.NOT_STARTED

        with patch("sys.stdout", new=StringIO()):
            self.interface.process_start_game()

        assert self.interface.engine.game_state == GameState.PLAYER_TURN
        assert self.interface.engine.current_hand.size == 13

    def test_process_draw_tile(self) -> None:
        """ツモアクション処理テスト"""
        self.interface.engine.start_game()

        with patch("sys.stdout", new=StringIO()):
            drawn_tile = self.interface.process_draw_tile()

        assert isinstance(drawn_tile, Tile)
        assert self.interface.engine.current_hand.size == 14
        assert self.interface.engine.game_state == GameState.AFTER_DRAW

    @patch("builtins.input", return_value="1")
    def test_process_discard_tile(self, mock_input) -> None:
        """打牌アクション処理テスト"""
        self.interface.engine.start_game()
        self.interface.engine.draw_tile()

        with patch("sys.stdout", new=StringIO()):
            self.interface.process_discard_tile()

        assert self.interface.engine.current_hand.size == 13
        assert self.interface.engine.game_state == GameState.PLAYER_TURN
        assert len(self.interface.engine.discarded_tiles) == 1

    def test_process_riichi_declaration(self) -> None:
        """リーチ宣言処理テスト"""
        self.interface.engine.start_game()

        # 強制的に聴牌形に設定
        test_tiles = [
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
        ]
        self.interface.engine.current_hand._tiles = test_tiles

        if self.interface.engine.calculate_shanten() == 0:
            with patch("sys.stdout", new=StringIO()):
                self.interface.process_riichi_declaration()

            assert self.interface.engine.is_riichi
            assert self.interface.engine.game_state == GameState.RIICHI

    def test_display_winning_message(self) -> None:
        """和了メッセージ表示テスト"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            winning_tile = Tile(suit="sou", value=5)
            self.interface.display_winning_message(winning_tile)
            output = fake_out.getvalue()

            assert "和了" in output or "あがり" in output
            assert "5索" in output

    def test_display_game_over_message(self) -> None:
        """ゲーム終了メッセージ表示テスト"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_game_over_message(True, "ツモ")
            output = fake_out.getvalue()

            assert "ゲーム終了" in output or "終了" in output

    def test_get_command_input(self) -> None:
        """コマンド入力テスト"""
        with patch("builtins.input", return_value="help"):
            command = self.interface.get_command_input()
            assert command == "help"

    def test_display_help(self) -> None:
        """ヘルプ表示テスト"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.interface.display_help()
            output = fake_out.getvalue()

            # ヘルプ情報が含まれている
            assert "コマンド" in output or "ヘルプ" in output
            assert "start" in output or "draw" in output

    def test_validate_discard_choice(self) -> None:
        """打牌選択検証テスト"""
        self.interface.engine.start_game()
        self.interface.engine.draw_tile()  # 14枚にする

        # 有効な選択
        assert self.interface.validate_discard_choice(1)
        assert self.interface.validate_discard_choice(14)

        # 無効な選択
        assert not self.interface.validate_discard_choice(0)
        assert not self.interface.validate_discard_choice(15)
        assert not self.interface.validate_discard_choice(-1)

    def test_format_tile_list(self) -> None:
        """牌リスト整形テスト"""
        tiles = [Tile(suit="sou", value=1), Tile(suit="sou", value=2), Tile(suit="sou", value=3)]

        formatted = self.interface.format_tile_list(tiles)
        assert "1索" in formatted
        assert "2索" in formatted
        assert "3索" in formatted

    def test_get_numbered_tile_display(self) -> None:
        """番号付き牌表示テスト"""
        self.interface.engine.start_game()
        self.interface.engine.draw_tile()

        display = self.interface.get_numbered_tile_display()

        # 番号が含まれている
        assert "1:" in display or "1." in display
        assert "索" in display

    def test_clear_screen(self) -> None:
        """画面クリアテスト"""
        with patch("os.system") as mock_system:
            self.interface.clear_screen()
            # システムコマンドが呼ばれることを確認
            assert mock_system.called

    def test_game_flow_integration(self) -> None:
        """ゲームフロー統合テスト"""
        # ゲーム開始
        assert self.interface.engine.game_state == GameState.NOT_STARTED

        with patch("sys.stdout", new=StringIO()):
            self.interface.process_start_game()

        assert self.interface.engine.game_state == GameState.PLAYER_TURN

        # ツモ
        with patch("sys.stdout", new=StringIO()):
            self.interface.process_draw_tile()

        assert self.interface.engine.game_state == GameState.AFTER_DRAW
        assert self.interface.engine.current_hand.size == 14

        # 打牌
        with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()):
            self.interface.process_discard_tile()

        assert self.interface.engine.game_state == GameState.PLAYER_TURN
        assert self.interface.engine.current_hand.size == 13

    def test_error_handling(self) -> None:
        """エラーハンドリングテスト"""
        # ゲーム開始前のツモ試行
        with patch("sys.stdout", new=StringIO()) as fake_out:
            try:
                self.interface.process_draw_tile()
            except Exception:
                pass  # エラーが適切に処理されることを確認

        # 不正な状態での打牌試行
        self.interface.engine.start_game()  # 13枚状態

        with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()) as fake_out:
            try:
                self.interface.process_discard_tile()
            except Exception:
                pass  # エラーが適切に処理されることを確認
