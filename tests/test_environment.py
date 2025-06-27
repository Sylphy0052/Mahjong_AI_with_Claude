"""開発環境の動作確認テスト"""

import sys


def test_python_version():
    """Pythonバージョンの確認"""
    assert sys.version_info >= (
        3,
        10,
    ), f"Python 3.10以上が必要です。現在のバージョン: {sys.version}"
    assert (
        sys.version_info.major == 3 and sys.version_info.minor >= 10
    ), f"Python 3.10以上が必要です。現在のバージョン: {sys.version}"


def test_basic_imports():
    """基本的なライブラリのインポート確認"""
    try:
        import dataclasses  # noqa: F401
        import json  # noqa: F401
        import random  # noqa: F401
        import typing  # noqa: F401

        assert True
    except ImportError as e:
        assert False, f"基本ライブラリのインポートに失敗: {e}"


def test_project_structure():
    """プロジェクト構造の確認"""
    import os

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 重要なディレクトリの存在確認
    assert os.path.exists(os.path.join(project_root, "src")), "srcディレクトリが存在しません"
    assert os.path.exists(os.path.join(project_root, "src", "mahjong_ai")), "src/mahjong_aiディレクトリが存在しません"
    assert os.path.exists(os.path.join(project_root, "tests")), "testsディレクトリが存在しません"
    assert os.path.exists(os.path.join(project_root, "docs")), "docsディレクトリが存在しません"

    # 重要なファイルの存在確認
    assert os.path.exists(os.path.join(project_root, "pyproject.toml")), "pyproject.tomlが存在しません"
    assert os.path.exists(os.path.join(project_root, "README.md")), "README.mdが存在しません"
    assert os.path.exists(os.path.join(project_root, "CLAUDE.md")), "CLAUDE.mdが存在しません"
