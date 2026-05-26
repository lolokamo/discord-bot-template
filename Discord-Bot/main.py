# ============================================================
#  main.py ― Bot のエントリーポイント（起動ファイル）
# ============================================================
#  このファイルが Bot の「スタート地点」です。
#  やっていることは大きく 3 つだけ:
#    1. .env からトークンを読む
#    2. Cogs/ フォルダの中の .py を全部読み込む
#    3. Bot を起動する
#
#  【起動方法】
#    pip install -r requirements.txt   ← 最初に1回だけ
#    python main.py                    ← これで起動！
# ============================================================

import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ── ログ（コンソールに出るメッセージ）の設定 ──
#  何が起きたか分かるように、時刻とレベル付きで表示します
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("bot")

# ── .env ファイルからトークンを読み込む ──
#  .env に「TOKEN=ここにトークン」と書いておくと、
#  os.getenv("TOKEN") で取得できます
load_dotenv()
TOKEN = os.getenv("TOKEN")

# トークンが無い場合はエラーを出して終了
if not TOKEN:
    log.critical("❌ .env ファイルに TOKEN が設定されていません！")
    sys.exit(1)

# ── 必須フォルダを自動作成 ──
#  初回起動時に Cogs/ と Data/ がなければ作ります
for folder in ["./Cogs", "./Data"]:
    os.makedirs(folder, exist_ok=True)

# ── Bot の初期化 ──
#  intents=all() → メンバー情報やメッセージ内容を全部取得できるようにする
#  command_prefix="!" → !reload のようなプレフィックスコマンドに使う
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


# ── Cogs（機能ファイル）を自動で読み込む関数 ──
async def load_cogs():
    # Cogs/ フォルダの中の .py ファイルを全部読み込む
    for filename in sorted(os.listdir("./Cogs")):
        # _で始まるファイル（__init__.py など）はスキップ
        if filename.startswith("_") or not filename.endswith(".py"):
            continue

        # 例: "admin.py" → "Cogs.admin" という名前で読み込む
        ext = f"Cogs.{filename[:-3]}"
        try:
            await bot.load_extension(ext)
            log.info("✅ Cog 読込OK: %s", ext)
        except Exception:
            log.exception("❌ Cog 読込NG: %s", ext)

    # スラッシュコマンド（/ping など）を Discord に登録する
    try:
        synced = await bot.tree.sync()
        log.info("✅ スラッシュコマンド %d 個を同期しました", len(synced))
    except Exception:
        log.exception("❌ スラッシュコマンドの同期に失敗しました")


# ↓ Bot が起動する直前に load_cogs() を呼ぶ設定
bot.setup_hook = load_cogs


# ── Bot が起動したら呼ばれるイベント ──
@bot.event
async def on_ready():
    log.info("🟢 Bot 起動完了: %s", bot.user)
    # ステータスを「testを視聴中」に設定
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="test"),
        status=discord.Status.online,
    )


# ── Bot を起動！ ──
bot.run(TOKEN, log_handler=None)
