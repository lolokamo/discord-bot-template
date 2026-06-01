# ============================================================
#  Cogs/verify.py ― 認証パネル（荒らし対策）
# ============================================================
#  /verify コマンドでパネルを設置 → メンバーがボタンを押す
#  → 指定したロールが付与される → 認証完了！
#
#  【使い方】
#    1. サーバーに「認証済み」などのロールを作っておく
#    2. /verify でパネルを設置（ロールを指定する）
#    3. メンバーがボタンを押すとロールが付与される
#
#  【荒らし対策の仕組み】
#    認証ロールが無いと他のチャンネルが見えないように
#    サーバーのチャンネル権限を設定しておけば、
#    ボタンを押さない限りサーバーを使えません。
#
#  【ロールIDの保存場所】
#    ボタンの custom_id に「verify:ロールID」として埋め込んでいます。
#    Embed にはロール情報を表示しないのでパネルがスッキリします。
# ============================================================

import discord
from discord.ext import commands
from discord import app_commands


# ── Cog 本体 ──
class Verify(commands.Cog):
    """認証パネル（荒らし対策）"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── ボタンが押されたときの処理 ──
    # custom_id が「verify:」で始まるボタンだけ反応する
    # Bot を再起動してもこの方式なら動き続ける
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # ボタン以外（スラッシュコマンドなど）は無視
        if interaction.type != discord.InteractionType.component:
            return

        # custom_id が「verify:」で始まらないボタンは無視
        custom_id = interaction.data.get("custom_id", "")
        if not custom_id.startswith("verify:"):
            return

        # custom_id からロールIDを取り出す（例: "verify:123456789" → 123456789）
        try:
            role_id = int(custom_id.split(":")[1])
        except (IndexError, ValueError):
            return

        role = interaction.guild.get_role(role_id)

        # ── ロールが見つからない場合 ──
        if not role:
            return await interaction.response.send_message(
                "❌ ロールが見つかりません。管理者に連絡してください。",
                ephemeral=True,   # ← 本人にしか見えないメッセージ
            )

        # ── すでに認証済みの場合 ──
        if role in interaction.user.roles:
            return await interaction.response.send_message(
                "✅ すでに認証済みです！",
                ephemeral=True,
            )

        # ── ロールを付与する ──
        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "✅ 認証が完了しました！",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot の権限が不足しています。管理者に連絡してください。",
                ephemeral=True,
            )

    # ── /verify コマンド ──
    @app_commands.command(name="verify", description="認証パネルを作成します")
    @app_commands.describe(
        role="認証時に付与するロール",
        title="パネルのタイトル（自由に変更OK）",
        description="パネルの説明文（自由に変更OK）",
    )
    @app_commands.default_permissions(administrator=True)   # 管理者のみ使える
    async def verify(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        title: str = "✅ 認証",
        description: str = "下のボタンを押して認証してください。\n認証するとサーバーのチャンネルが表示されます。",
    ):
        # ── パネル用の Embed（埋め込みメッセージ）を作成 ──
        # ロール情報は表示せず、シンプルなパネルにする
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green(),
        )

        # ── ボタンを作成 ──
        # custom_id にロールIDを埋め込む（例: "verify:123456789"）
        view = discord.ui.View(timeout=None)
        button = discord.ui.Button(
            label="✅ 認証する",
            style=discord.ButtonStyle.success,
            custom_id=f"verify:{role.id}",        # ← ここにロールIDを保存！
        )
        view.add_item(button)

        # ── パネルを送信 ──
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ 認証パネルを作成しました！", ephemeral=True)


# ============================================================
#  ↓ これが無いと Cog が読み込まれない！
# ============================================================
async def setup(bot: commands.Bot):
    await bot.add_cog(Verify(bot))
