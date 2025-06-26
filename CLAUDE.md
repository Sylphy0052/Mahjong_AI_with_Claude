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
| Phase 1 | CUI版1人用麻雀（索子のみ） | 開発予定 |
| Phase 2 | Webアプリケーション化 | 未着手 |
| Phase 3 | 2人用麻雀への拡張 | 未着手 |
| Phase 4 | 簡易AI実装 | 未着手 |
| Phase 5 | 4人用麻雀への拡張 | 未着手 |
| Phase 6 | AI高度化 | 未着手 |

## 開発セットアップ

- **プログラミング言語**: Python 3.11
- **フレームワーク**: Flask（Phase 2以降）
- **データベース**: SQLite
- **依存関係管理**: Poetry
- **テストフレームワーク**: pytest
- **フロントエンド**: TypeScript + React（Phase 2以降）

## プロジェクト構造

```bash
Mahjong_AI_with_Claude/
├── docs/               # ドキュメント
│   └── claude/        # CLAUDE Codeで作成した指示書
│       └── 開発仕様書.md  # 詳細な開発仕様書
├── src/               # ソースコード
│   └── mahjong_ai/    # メインパッケージ
├── tests/             # テストコード
├── scripts/           # ユーティリティスクリプト
├── .gitignore
├── pyproject.toml     # Poetry設定
└── README.md
```

## 開発コマンド

### 環境セットアップ

```bash
# Poetryのインストール（未インストールの場合）
curl -sSL https://install.python-poetry.org | python3 -

# 依存関係のインストール
poetry install

# 仮想環境のアクティベート
poetry shell
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
```

## アーキテクチャの考慮事項

この麻雀AIを開発する際：

1. **ゲームロジック**: 麻雀の基本ルールとゲーム状態管理の実装
2. **AIコンポーネント**: AI意思決定システムの設計
3. **Claude統合**: Claudeの機能を統合する方法の計画
4. **ユーザーインターフェース**: CLI、GUI、またはWebインターフェースが必要かの決定

## 現在の開発段階: Phase 1

### Phase 1: CUI版1人用麻雀（索子のみ）

#### 基本仕様

- **使用牌**: 索子のみ（1〜9、各4枚、合計36枚）
- **プレイヤー数**: 1人
- **初期手牌**: 13枚
- **和了形式**: 4面子1雀頭、七対子
- **実装機能**: ツモ、打牌、リーチ、暗槓、和了判定

#### データ構造

- **牌の表現**: 辞書型 `{'suit': 'sou', 'value': 1-9}`
- **内部ID**: 数値ID（0-35）で管理
- **手牌管理**: リスト（List[Tile]）、常時ソート状態

#### 主要アルゴリズム

- **和了判定**: 再帰的探索（通常形）+ 七対子判定
- **向聴数計算**: 通常形・七対子の最小値
- **UI**: CUIベースの対話型インターフェース

#### 実装予定の機能

1. 牌クラスの実装
2. 手牌管理システム
3. 和了判定ロジック
4. 向聴数計算
5. CUIインターフェース
6. ゲームフロー制御

## 開発ワークフロー

1. テスト駆動開発（TDD）で進める
2. 機能追加前にテストを作成
3. コミット前にすべてのテストが通ることを確認
4. コード品質ツールを実行してクリーンなコードを維持

## 参考資料

詳細な仕様書: `docs/claude/開発仕様書.md`
