# MahjongAI - Claudeと統合した麻雀AI

段階的な開発手法を用いて、最終的に人間と対戦可能な麻雀AIを作成するプロジェクトです。

## プロジェクト概要

### 目的

- **主目的**: 段階的な開発手法を用いて、最終的に人間と対戦可能な麻雀AIを作成する
- **副次的目的**: AI・機械学習技術の段階的な学習と実装

### 開発スケジュール

| フェーズ | 内容 |
|---------|------|
| Phase 1 | CUI版1人用麻雀（索子のみ） |
| Phase 2 | Webアプリケーション化 |
| Phase 3 | 2人用麻雀への拡張 |
| Phase 4 | 簡易AI実装 |
| Phase 5 | 4人用麻雀への拡張 |
| Phase 6 | AI高度化 |

## 技術スタック

### バックエンド

- **言語**: Python 3.11
- **フレームワーク**: Flask
- **データベース**: SQLite
- **テスト**: pytest

### フロントエンド（Phase 2以降）

- **言語**: TypeScript
- **フレームワーク**: React
- **UIライブラリ**: Ant Design
- **状態管理**: Zustand

## 開発環境

- **OS**: Windows 11 + WSL
- **IDE**: VSCode
- **バージョン管理**: GitHub
- **依存関係管理**: Poetry

## 開発手順

1. Web Claudeで仕様書を作成(@docs/claude/開発仕様書.md)
2. プロジェクト構造の設定
3. Phase 1: CUI版1人用麻雀の実装
4. 段階的な機能拡張

## セットアップ

```bash
# 依存関係のインストール
poetry install

# 仮想環境のアクティベート
poetry shell

# テストの実行
poetry run pytest
```

詳細な仕様については [@docs/claude/開発仕様書.md](docs/claude/開発仕様書.md) を参照してください。
