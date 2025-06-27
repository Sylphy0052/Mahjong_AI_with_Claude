# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code) へのガイダンスを提供します。

## プロジェクト概要

MahjongAI - 段階的な開発手法を用いて、最終的に人間と対戦可能な麻雀AIを作成するプロジェクトです。

### 目的

- **主目的**: 段階的な開発手法を用いて、最終的に人間と対戦可能な麻雀AIを作成する
- **副次的目的**: AI・機械学習技術の段階的な学習と実装

### 開発段階（Phase）

| フェーズ | 内容 | 状態 |
|---------|------|------|
| Phase 1 | CUI版1人用麻雀（索子のみ） | ✅ **完了** |
| Phase 2 | Webアプリケーション化 | 未着手 |
| Phase 3 | 2人用麻雀への拡張 | 未着手 |
| Phase 4 | 簡易AI実装 | 未着手 |
| Phase 5 | 4人用麻雀への拡張 | 未着手 |
| Phase 6 | AI高度化 | 未着手 |

## 開発セットアップ

- **プログラミング言語**: Python 3.10.12 ✅
- **フレームワーク**: Flask（Phase 2以降）
- **データベース**: SQLite
- **依存関係管理**: Poetry ✅
- **テストフレームワーク**: pytest ✅
- **開発ツール**: Black, isort, flake8, mypy ✅
- **フロントエンド**: TypeScript + React（Phase 2以降）

## プロジェクト構造

```bash
Mahjong_AI_with_Claude/
├── docs/               # ドキュメント
│   └── claude/        # CLAUDE Codeで作成した指示書
│       ├── 開発仕様書.md  # 詳細な開発仕様書
│       ├── phase1.md  # Phase 1実装方針
│       ├── phase1_implementation_report.md  # 旧完了報告
│       ├── phase1_final_implementation_report.md  # 最終報告書
│       └── phase1_post_implementation_updates.md  # 更新記録
├── src/               # ソースコード
│   └── mahjong_ai/    # メインパッケージ
│       ├── models/    # データモデル（Tile, Hand）
│       ├── logic/     # ゲームロジック（WinningChecker, ShantenCalculator）
│       ├── game/      # ゲーム管理（WallTiles, GameEngine）
│       ├── interface/ # UI（CUIInterface）
│       └── utils/     # ユーティリティ（Logger）
├── tests/             # テストコード
├── logs/              # ログ出力ディレクトリ
├── scripts/           # ユーティリティスクリプト
├── .gitignore
├── pyproject.toml     # Poetry設定
└── README.md
```

## 開発コマンド

### 環境セットアップ

```bash
# Poetry環境のセットアップ（初回のみ）
export PATH="/home/sylphy/.local/bin:$PATH"
poetry install

# 開発ツールの実行
poetry run python scripts/dev.py
```

### テスト実行

```bash
# すべてのテストを実行
poetry run pytest

# カバレッジ付きでテスト実行
poetry run pytest --cov

# 特定のテストファイルを実行
poetry run pytest tests/test_specific.py

# 特定のテスト関数を実行
poetry run pytest tests/test_specific.py::test_function_name
```

### コード品質

```bash
# コードフォーマット（Black）
poetry run black src tests

# インポート順序の整理（isort）
poetry run isort src tests

# リント（flake8）
poetry run flake8 src tests

# 型チェック（mypy）
poetry run mypy src

# 全ツール一括実行
poetry run python scripts/dev.py
```

## アーキテクチャの考慮事項

この麻雀AIを開発する際：

1. **ゲームロジック**: 麻雀の基本ルールとゲーム状態管理の実装
2. **AIコンポーネント**: AI意思決定システムの設計
3. **Claude統合**: Claudeの機能を統合する方法の計画
4. **ユーザーインターフェース**: CLI、GUI、またはWebインターフェースが必要かの決定

## Phase 1: 実装完了 ✅

### 📊 実装状況サマリー

- **コア機能**: 100% 完了
- **追加機能**: 暗槓・ツモ和了選択制・包括的ログ実装
- **テストカバレッジ**: 64%（新機能追加により一部更新必要）
- **実装品質**: TDD・型アノテーション・PyDoc完備
- **実行状況**: 完全動作・本格的麻雀ゲーム体験提供

### 🚀 最新の追加機能（2025年6月）

- **暗槓システム**: 4枚同牌での暗槓・嶺上牌ツモ・嶺上開花対応
- **ツモ和了選択制**: 強制和了廃止・プレイヤー選択による和了実行
- **リーチシステム改修**: 打牌時同時宣言・正式ルール準拠
- **包括的ログシステム**: タイムスタンプ付き詳細操作記録
- **UI改善**: 動的アクション選択・視覚的な牌マーキング

### Phase 1: CUI版1人用麻雀（索子のみ）

#### 実装された仕様

- **使用牌**: 索子のみ（1〜9、各6枚、合計54枚）
- **プレイヤー数**: 1人
- **初期手牌**: 13枚
- **和了形式**: 4面子1雀頭、七対子、暗槓対応
- **実装機能**: ツモ、打牌、リーチ、暗槓、ツモ和了選択、和了判定、向聴数計算

#### 実装完了コンポーネント

1. **Tileクラス**: イミュータブルな牌データ構造
2. **Handクラス**: 自動ソート付き手牌管理（最大14枚）
3. **WinningCheckerクラス**: 通常形・七対子・暗槓対応の和了判定
4. **ShantenCalculatorクラス**: 効率的な向聴数計算
5. **WallTilesクラス**: 山牌管理・嶺上牌対応・シャッフル・抽選機能
6. **GameEngineクラス**: ゲーム状態管理・進行制御・暗槓・ツモ和了選択
7. **CUIInterfaceクラス**: 対話型コマンドラインUI・高度なアクション選択
8. **Loggerクラス**: 包括的ログシステム・タイムスタンプ付き記録

#### 実装された機能

- ✅ **ゲーム開始**: 13枚の初期配牌
- ✅ **ツモ**: 山牌から1枚抽選
- ✅ **打牌**: 14枚から1枚選択して除去
- ✅ **リーチ宣言**: 打牌時同時宣言（番号+r形式）
- ✅ **暗槓**: 4枚同牌での暗槓実行・嶺上ツモ
- ✅ **ツモ和了選択**: 強制和了廃止・プレイヤー選択制
- ✅ **和了判定**: 通常形・七対子・暗槓対応
- ✅ **向聴数表示**: リアルタイム計算・表示
- ✅ **待ち牌表示**: 聴牌時の和了牌情報
- ✅ **包括的ログ**: 全操作・状態の詳細記録
- ✅ **ゲーム終了**: 和了・流局の適切な処理
- ✅ **エラーハンドリング**: 不正操作の防止
- ✅ **ヘルプシステム**: ゲームルール説明

#### ゲーム実行方法

```bash
# Poetry環境セットアップ（初回のみ）
poetry install

# メインゲーム実行
poetry run python main.py

# テスト実行
poetry run pytest                           # 全テスト実行（一部更新必要）
poetry run python scripts/test_simple.py all # 簡易テスト
poetry run python run_all_tests.py         # 統合テスト

# 新機能のテスト
poetry run python test_kan_functionality.py # 暗槓機能テスト
poetry run python test_optional_win.py     # ツモ和了選択テスト
```

#### 技術特徴

- **TDD（テスト駆動開発）**: 全コンポーネントでテスト先行
- **型アノテーション**: 100%の関数・メソッドで型明示
- **PyDoc**: Google形式の包括的ドキュメンテーション
- **アーキテクチャ**: レイヤー分離による拡張可能な設計
- **パフォーマンス**: 和了判定10ms以内（仕様書要件達成）

#### ドキュメント

- **実装方針**: `docs/claude/phase1.md`
- **旧完了報告**: `docs/claude/phase1_implementation_report.md`
- **最終実装報告**: `docs/claude/phase1_final_implementation_report.md`
- **実装後の更新記録**: `docs/claude/phase1_post_implementation_updates.md`

## コーディング規約

### 型アノテーション

- **必ず型を明記すること**
- 関数の引数、戻り値、クラス属性にすべて型アノテーションを付ける
- `typing`モジュールの型ヒントを積極的に活用する

```python
from typing import List, Dict, Optional, Union

def calculate_shanten(tiles: List[Tile]) -> int:
    """向聴数を計算する"""
    pass

class Hand:
    """手牌クラス"""
    tiles: List[Tile]
    is_riichi: bool

    def __init__(self, tiles: List[Tile]) -> None:
        self.tiles = tiles
        self.is_riichi = False
```

### ドキュメンテーション

- **必ずPyDocを書くこと**
- すべてのクラス、関数、メソッドにdocstringを記述する
- Google形式のdocstringを使用する

```python
def is_winning_hand(tiles: List[Tile]) -> bool:
    """手牌が和了形かどうかを判定する

    Args:
        tiles: 判定対象の牌のリスト（14枚）

    Returns:
        和了形の場合True、そうでなければFalse

    Raises:
        ValueError: 牌数が14枚でない場合

    Examples:
        >>> tiles = [Tile('sou', 1), Tile('sou', 1), ...]
        >>> is_winning_hand(tiles)
        True
    """
    if len(tiles) != 14:
        raise ValueError("牌数は14枚である必要があります")
    return _check_normal_form(tiles) or _check_seven_pairs(tiles)
```

### その他の規約

- クラス名: PascalCase (`TileType`, `GameState`)
- 関数・変数名: snake_case (`calculate_shanten`, `is_winning`)
- 定数: UPPER_SNAKE_CASE (`MAX_TILES`, `SUIT_TYPES`)
- プライベートメソッド: アンダースコア接頭辞 (`_check_pairs`)

## 開発ワークフロー

1. テスト駆動開発（TDD）で進める
2. 機能追加前にテストを作成
3. コミット前にすべてのテストが通ることを確認
4. コード品質ツールを実行してクリーンなコードを維持
5. 型チェック（mypy）とdocstringの記述を必須とする

## 参考資料

詳細な仕様書: `docs/claude/開発仕様書.md`
