# ============================================================
#  Data/data_manager.py ― データの読み書きユーティリティ
# ============================================================
#  Bot が覚えておきたいデータ（警告数、レベルなど）を
#  JSON ファイルとして Data/ フォルダに保存・読込する関数です。
#
#  【使い方（Cog の中で）】
#    from Data import load, save
#
#    # 読み込み（ファイルが無ければ空の {} が返る）
#    data = load("warns.json")
#
#    # 書き込み
#    data["12345"] = {"count": 3}
#    save("warns.json", data)
# ============================================================

import json
import os
from pathlib import Path

# Data フォルダのパス
DATA_DIR = Path("./Data")


def load(filename: str) -> dict:
    """
    JSON ファイルを読み込んで辞書（dict）を返す。
    ファイルが存在しなければ空の辞書 {} を返す。
    """
    filepath = DATA_DIR / filename

    # ファイルが無ければ空の辞書を返す（エラーにならない）
    if not filepath.exists():
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save(filename: str, data: dict) -> None:
    """
    辞書（dict）を JSON ファイルに保存する。
    indent=2 で見やすく整形して保存する。
    """
    # Data フォルダが無ければ作る
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        # ensure_ascii=False → 日本語がそのまま保存される
        json.dump(data, f, ensure_ascii=False, indent=2)
