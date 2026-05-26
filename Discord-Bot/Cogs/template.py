# ============================================================
#  Cogs/template.py ― Cog のテンプレート（ひな形）
# ============================================================
#  新しい機能を作りたいときは、このファイルをコピーして
#  名前を変えて使ってください。
#
#  例: Cogs/greeting.py にコピー → !reload で反映
#
#  ⚠️ このファイル自体は使わないので、
#     不要なら削除しても大丈夫です。
# ============================================================

import discord
from discord.ext import commands
from discord import app_commands

# もしデータの保存が必要なら ↓ のコメントを外す
# from Data import load, save


class Template(commands.Cog):
    """
    Cog の説明をここに書く。
    この文字列は /help コマンドなどで表示されます。
    """

    def __init__(self, bot: commands.Bot):
        # bot を保存しておくと、Cog の中で bot の機能が使える
        self.bot = bot

    # ── スラッシュコマンドの例 ──
    # Discord で /hello と打つと反応する
    @app_commands.command(name="hello", description="挨拶するコマンド")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("こんにちは！👋")

    # ── プレフィックスコマンドの例 ──
    # Discord で !hi と打つと反応する
    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context):
        await ctx.send("やっほー！")

    # ── イベントの例 ──
    # 誰かがメッセージを送るたびに呼ばれる
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bot 自身のメッセージは無視する（無限ループ防止）
        if message.author.bot:
            return
        # ここに処理を書く（例: 特定の言葉に反応する）


# ============================================================
#  ↓ これが無いと Cog が読み込まれないので必ず書く！
# ============================================================
async def setup(bot: commands.Bot):
    await bot.add_cog(Template(bot))
