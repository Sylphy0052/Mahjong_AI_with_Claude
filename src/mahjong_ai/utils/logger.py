"""ログ設定モジュール - デバッグ用ログシステム"""

import datetime
import logging
import os
from pathlib import Path
from typing import Optional


class GameLogger:
    """ゲーム実行ログを管理するクラス"""
    
    _instance: Optional['GameLogger'] = None
    
    def __new__(cls) -> 'GameLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """ログ設定を初期化"""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # ログディレクトリの作成
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # タイムスタンプベースのファイル名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"mahjong_game_{timestamp}.log"
        
        # ロガーの設定
        self.logger = logging.getLogger("MahjongGame")
        self.logger.setLevel(logging.DEBUG)
        
        # 既存のハンドラーをクリア
        self.logger.handlers.clear()
        
        # ファイルハンドラーの設定
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # コンソールハンドラーの設定
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # フォーマッターの設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # ハンドラーを追加
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"ログシステム初期化完了: {self.log_file}")
    
    def get_logger(self) -> logging.Logger:
        """ロガーインスタンスを取得"""
        return self.logger
    
    def log_game_state(self, engine) -> None:
        """ゲーム状態の詳細ログ"""
        logger = self.get_logger()
        logger.info("=" * 50)
        logger.info("ゲーム状態詳細:")
        logger.info(f"  状態: {engine.game_state}")
        logger.info(f"  ターン数: {engine.turn_count}")
        logger.info(f"  リーチフラグ: {engine.is_riichi}")
        logger.info(f"  手牌枚数: {engine.current_hand.size}")
        logger.info(f"  手牌内容: {engine.current_hand}")
        logger.info(f"  山牌残り: {engine.wall.remaining_count}")
        logger.info(f"  捨て牌: {[str(t) for t in engine.discarded_tiles]}")
        logger.info(f"  向聴数: {engine.calculate_shanten()}")
        logger.info(f"  can_draw(): {engine.can_draw()}")
        logger.info(f"  can_discard(): {engine.can_discard()}")
        logger.info(f"  can_riichi(): {engine.can_riichi()}")
        logger.info("=" * 50)
    
    def log_action(self, action: str, details: str = "") -> None:
        """アクション実行ログ"""
        logger = self.get_logger()
        logger.info(f"アクション実行: {action}")
        if details:
            logger.info(f"  詳細: {details}")
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """エラーログ"""
        logger = self.get_logger()
        logger.error(f"エラー発生: {error}")
        if context:
            logger.error(f"  コンテキスト: {context}")
        logger.error(f"  エラー型: {type(error).__name__}")
        import traceback
        logger.error(f"  スタックトレース:\n{traceback.format_exc()}")
    
    def log_ui_action(self, menu_type: str, choice: int, available_choices: int) -> None:
        """UI操作ログ"""
        logger = self.get_logger()
        logger.info(f"UI操作: {menu_type}")
        logger.info(f"  選択: {choice}/{available_choices}")


# グローバルインスタンス
game_logger = GameLogger()


def get_logger() -> logging.Logger:
    """ゲームロガーを取得（簡易アクセス用）"""
    return game_logger.get_logger()


def log_game_state(engine) -> None:
    """ゲーム状態ログ（簡易アクセス用）"""
    game_logger.log_game_state(engine)


def log_action(action: str, details: str = "") -> None:
    """アクションログ（簡易アクセス用）"""
    game_logger.log_action(action, details)


def log_error(error: Exception, context: str = "") -> None:
    """エラーログ（簡易アクセス用）"""
    game_logger.log_error(error, context)


def log_ui_action(menu_type: str, choice: int, available_choices: int) -> None:
    """UI操作ログ（簡易アクセス用）"""
    game_logger.log_ui_action(menu_type, choice, available_choices)