#!/usr/bin/env python3
"""シンプルなテストランナー（pytest無しでテスト実行用）"""

import importlib.util
import os
import sys
import traceback


def run_tests():
    """テストディレクトリのテストを実行"""
    test_dir = "tests"
    test_files = []

    # テストファイルを検索
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))

    passed = 0
    failed = 0

    for test_file in test_files:
        print(f"\n=== {test_file} ===")

        # モジュールをインポート
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        test_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(test_module)

            # test_で始まる関数を実行
            for attr_name in dir(test_module):
                if attr_name.startswith("test_"):
                    test_func = getattr(test_module, attr_name)
                    try:
                        test_func()
                        print(f"✓ {attr_name}")
                        passed += 1
                    except Exception as e:
                        print(f"✗ {attr_name}: {e}")
                        failed += 1

        except Exception as e:
            print(f"モジュールの読み込みエラー: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n=== テスト結果 ===")
    print(f"成功: {passed}")
    print(f"失敗: {failed}")
    print(f"合計: {passed + failed}")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
