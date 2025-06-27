# 麻雀AI with Claude

段階的な開発手法を用いて、最終的に人間と対戦可能な麻雀AIを作成するプロジェクトです。

## 🎯 プロジェクト概要

### 主要目的

- 段階的な開発手法による麻雀AIの作成
- AI・機械学習技術の段階的な学習と実装
- Claude Codeとの協調による高品質な開発

### 開発段階（Phase）

| フェーズ | 内容 | 状態 |
|---------|------|------|
| **Phase 1** | **CUI版1人用麻雀（索子のみ）** | **✅ 完了** |
| Phase 2 | Webアプリケーション化 | 🔄 未着手 |
| Phase 3 | 2人用麻雀への拡張 | 🔄 未着手 |
| Phase 4 | 簡易AI実装 | 🔄 未着手 |
| Phase 5 | 4人用麻雀への拡張 | 🔄 未着手 |
| Phase 6 | AI高度化 | 🔄 未着手 |

## 🎮 Phase 1: 完成機能

### 実装された機能

- ✅ **完全なゲームフロー**: ゲーム開始・ツモ・打牌・和了判定
- ✅ **和了判定**: 通常形（4面子1雀頭）・七対子対応
- ✅ **向聴数計算**: リアルタイム表示
- ✅ **リーチ機能**: 聴牌時の宣言
- ✅ **待ち牌表示**: 聴牌時の和了牌情報
- ✅ **対話型UI**: 直感的なコマンドラインインターフェース
- ✅ **エラーハンドリング**: 不正操作の防止
- ✅ **ヘルプシステム**: ゲームルール説明

### 技術的特徴

- **TDD（テスト駆動開発）**: 全コンポーネントでテスト先行
- **型アノテーション**: 100%の関数・メソッドで型明示
- **PyDoc**: Google形式の包括的ドキュメンテーション
- **アーキテクチャ**: レイヤー分離による拡張可能な設計
- **パフォーマンス**: 和了判定10ms以内

## 🚀 クイックスタート

### 環境要件

- Python 3.11
- Poetry

### 環境セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd Mahjong_AI_with_Claude

# Poetry環境のセットアップ
poetry install

# Poetry環境をアクティベート
poetry shell
```

### ゲーム実行

```bash
# Poetry環境でゲームを開始
poetry run python main.py
```

### テスト実行

```bash
# Poetry + pytest による正式テスト
poetry run pytest                    # 全テスト実行
poetry run pytest --cov             # カバレッジ付きテスト
poetry run pytest tests/test_tile.py -v  # 個別テスト

# 簡易テストランナー
poetry run python scripts/test_simple.py all      # 全テスト
poetry run python scripts/test_simple.py tile     # 牌クラス
poetry run python scripts/test_simple.py hand     # 手牌管理
poetry run python scripts/test_simple.py winning  # 和了判定
poetry run python scripts/test_simple.py shanten  # 向聴数計算
poetry run python scripts/test_simple.py wall     # 山牌管理
poetry run python scripts/test_simple.py engine   # ゲームエンジン
poetry run python scripts/test_simple.py cui      # CUIインターフェース

# 統合テストランナー
poetry run python run_all_tests.py  # 全テスト（詳細出力）
```

## 🏗️ アーキテクチャ

### コンポーネント構成

```
┌─────────────────────────┐
│   CUIInterface (UI)     │  ← ユーザーインターフェース
├─────────────────────────┤
│   GameEngine (Game)     │  ← ゲームフロー制御
├─────────────────────────┤
│ WinningChecker/Shanten │  ← 麻雀ルール・判定
│     (Logic)             │
├─────────────────────────┤
│   Tile/Hand/WallTiles   │  ← データ構造・状態管理
│     (Models)            │
└─────────────────────────┘
```

### 主要クラス

1. **Tile（牌）**: 索子1-9の麻雀牌を表現するイミュータブルクラス
2. **Hand（手牌）**: 最大14枚の手牌管理、自動ソート機能
3. **WallTiles（山牌）**: 54枚の山牌管理、シャッフル・抽選機能
4. **WinningChecker（和了判定）**: 通常形・七対子の和了判定
5. **ShantenCalculator（向聴数計算）**: 効率的な向聴数計算
6. **GameEngine（ゲームエンジン）**: ゲーム状態管理・進行制御
7. **CUIInterface（UI）**: コマンドライン対話型インターフェース

## 📁 プロジェクト構造

```
Mahjong_AI_with_Claude/
├── src/                     # ソースコード
│   └── mahjong_ai/
│       ├── models/          # データ構造
│       │   ├── tile.py      # 牌クラス
│       │   └── hand.py      # 手牌クラス
│       ├── logic/           # ゲームロジック
│       │   ├── winning_checker.py   # 和了判定
│       │   └── shanten_calculator.py # 向聴数計算
│       ├── game/            # ゲーム管理
│       │   ├── wall_tiles.py    # 山牌管理
│       │   └── game_engine.py   # ゲームエンジン
│       └── interface/       # ユーザーインターフェース
│           └── cui_interface.py # CUIインターフェース
├── tests/                   # テストコード
├── docs/                    # ドキュメント
│   └── claude/              # 開発ドキュメント
├── main.py                  # メインエントリーポイント
├── test_*_runner.py         # テストランナー
└── README.md               # 本ファイル
```

## 🎲 ゲームの遊び方

### 基本ルール

- **目標**: 14枚で和了形を作る
- **和了形**: 4面子1雀頭 または 七対子
- **使用牌**: 索子のみ（1索〜9索、各6枚）

### 操作方法

1. **ゲーム開始**: メニューから「1. ゲーム開始」を選択
2. **ツモ**: 13枚から山牌の1枚を引いて14枚にする
3. **打牌**: 14枚から1枚を選んで捨てて13枚に戻す
4. **リーチ**: 聴牌時（0向聴）に宣言可能
5. **和了**: 14枚が和了形になったら自動判定

### 画面の見方

```
ゲーム状態: プレイヤーターン
ターン数: 5
山牌残り: 35枚

手牌(13枚): 1索 2索 3索 4索 5索 6索 7索 8索 9索 1索 1索 1索 2索
聴牌中です！
待ち牌: 3索

1. ツモ
2. リーチ宣言
```

## 📚 ドキュメント

- **[開発仕様書](docs/claude/開発仕様書.md)**: 詳細な仕様とルール
- **[Phase 1実装方針](docs/claude/phase1.md)**: 設計思想とアーキテクチャ
- **[Phase 1完了報告](docs/claude/phase1_implementation_report.md)**: 実装結果詳細
- **[プロジェクト設定](CLAUDE.md)**: 開発環境と設定

## 🧪 開発・テスト

### 開発ツール

```bash
# コードフォーマット
poetry run black src tests

# インポート整理
poetry run isort src tests

# リント
poetry run flake8 src tests

# 型チェック
poetry run mypy src

# 全ツール実行
poetry run python scripts/dev.py
```

### テスト戦略

- **単体テスト**: 各クラス・メソッドの個別テスト
- **結合テスト**: コンポーネント間の連携テスト
- **統合テスト**: ゲーム全体のシナリオテスト

## 🔮 次期開発予定

### Phase 2: Webアプリケーション化

- Flaskによるウェブ化
- TypeScript + Reactフロントエンド
- リアルタイム更新

### Phase 3以降

- 2人用麻雀への拡張
- 簡易AI実装
- 4人用麻雀への拡張
- AI高度化

## 🤝 貢献

このプロジェクトはClaude Codeとの協調開発により進行しています。

### 開発方針

- **TDD**: テスト駆動開発の徹底
- **型安全性**: 100%の型アノテーション
- **ドキュメント化**: 包括的なドキュメンテーション
- **段階的開発**: 小さな成功の積み重ね

## 📄 ライセンス

[ライセンス情報を追加予定]

## 🎉 実績

- ✅ **Phase 1完了**: 完全にプレイ可能な麻雀ゲーム
- ✅ **TDD実装**: 包括的なテストカバレッジ
- ✅ **高品質コード**: 型安全性とドキュメンテーション
- ✅ **アーキテクチャ**: 拡張可能な設計

---

**Phase 1完了！ 🎊**

索子のみながら、完全にプレイ可能な麻雀ゲームが誕生しました。TDD方式による高品質な実装で、Phase 2以降の拡張に向けた強固な基盤が完成しています。
