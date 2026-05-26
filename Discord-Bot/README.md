# Discord 汎用 Bot（初心者向け）

## このBotについて

Cogs（コグ）というしくみで **機能を自由に追加・削除できる** Discord Bot です。  
`Cogs/` フォルダに `.py` ファイルを入れるだけで機能が追加されます。

---

## フォルダ構成

```
.
├── main.py              ← Bot の起動ファイル（ここから始まる）
├── .env                 ← トークンを書くファイル（絶対に他人に見せない！）
├── requirements.txt     ← 必要なライブラリの一覧
├── .gitignore           ← Git にアップしないファイルの設定
│
├── Cogs/                ← 機能ファイルを入れるフォルダ
│   ├── __init__.py      ← Python がフォルダを認識するためのファイル（空でOK）
│   └── template.py      ← 新しい Cog を作るときのひな形
│
└── Data/                ← Bot が使うデータの保存先
    ├── __init__.py      ← Python がフォルダを認識するためのファイル
    └── data_manager.py  ← データを読み書きする便利関数
```

---

## セットアップ手順（初めての人向け）

### 1. Python をインストール

https://www.python.org/downloads/ から Python 3.10 以上をインストール。  
インストール時に **「Add Python to PATH」にチェック** を入れてください。

### 2. ライブラリをインストール

ターミナル（コマンドプロンプト）を開いて、このフォルダで:

```bash
pip install -r requirements.txt
```

### 3. トークンを設定

`.env` ファイルを開いて、`ここにトークンを貼り付け` の部分を  
Discord Developer Portal で取得したトークンに置き換えてください。

```
TOKEN=MTE2xxxxxxxxxxxxxxxxxxxxxxxx
```

**トークンの取得方法:**
1. https://discord.com/developers/applications にアクセス
2. 「New Application」→ 名前を入力 → 作成
3. 左メニュー「Bot」→「Reset Token」→ コピー

### 4. Bot をサーバーに招待

1. Developer Portal → 左メニュー「OAuth2」→「URL Generator」
2. SCOPES: `bot`, `applications.commands` にチェック
3. BOT PERMISSIONS: 必要な権限にチェック（管理者なら全部OK）
4. 生成された URL をブラウザで開いて招待

### 5. 起動！

```bash
python main.py
```

`🟢 Bot 起動完了` と表示されれば成功です！

---

## 機能の追加方法

1. `Cogs/template.py` をコピーして名前を変える（例: `Cogs/greeting.py`）
2. 中身を編集する
3. Bot を再起動するか、`!reload` コマンドで反映

---

## データの保存方法（Cog の中で使う）

```python
from Data import load, save

# 読み込み（ファイルが無ければ {} が返る）
data = load("example.json")

# データを追加
data["user_123"] = {"level": 5, "exp": 120}

# 保存（Data/example.json に保存される）
save("example.json", data)
```

---

## Discord で Bot を販売するときに送れるファイル

Discord のチャットやDMでファイルを送信して納品できます。

### 送れるファイル形式

| 種類 | 拡張子 | 説明 |
|------|--------|------|
| **Python ファイル** | `.py` | Cog やメインファイル（テキストなので軽い） |
| **JSON ファイル** | `.json` | 設定データ |
| **テキスト** | `.txt` `.md` | 説明書・README |
| **画像** | `.png` `.jpg` `.gif` | Bot のアイコンなど |
| **圧縮ファイル** | `.zip` | 複数ファイルをまとめて送る場合 |

### サイズ制限

| プラン | 上限 |
|--------|------|
| **無料ユーザー** | **10MB** まで |
| **Nitro Basic** | **50MB** まで |
| **Nitro** | **500MB** まで |

### おすすめの納品方法

**方法① ZIP にまとめて Discord で送る（簡単）**
```
Bot一式.zip（通常 数十KB〜数MB で収まる）
  ├── main.py
  ├── .env.example    ← トークンは空にしておく！
  ├── requirements.txt
  ├── Cogs/
  │   └── ○○.py
  └── Data/
      └── data_manager.py
```
→ Python ファイルだけなら 10MB に余裕で収まります。

**方法② GitHub の非公開リポジトリを共有**
→ 大きいファイルがあるときや、アップデートを配布したいとき向け。

### ⚠️ 販売時の注意

- `.env`（トークン入り）は **絶対に送らない**！ → `.env.example` を代わりに送る
- 購入者に「トークンは自分で取得して .env に貼ってね」と伝える
- Bot のソースコードは著作物です。無断転売禁止など規約を決めておくと安心
