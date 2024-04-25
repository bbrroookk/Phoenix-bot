import discord
from discord import app_commands
from discord.ext import commands
import sqlite3


conn = sqlite3.connect("data/data.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS auto_channels (channel_id INTREGER, url TEXT, tahwil BOOL) ")
conn.commit()

class autoline(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  autoline = app_commands.Group(name='autoline', description='set autoline')


  @autoline.command(name="set", description="set autoline for this channel")
  @app_commands.describe(url='رابط الصورة', tahwil='هل الرووم للتحويلات؟')
  async def auto(self, inter: discord.Interaction, url: str, tahwil: bool=False):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("sorry, only admins can do that", ephemeral=True)
      return

    channel = inter.channel
    await inter.response.send_message(f' autoline set to {channel.mention} ', ephemeral=True)
    c.execute("INSERT OR REPLACE INTO auto_channels VALUES (?,?,?)", (channel.id, url, tahwil) )
    conn.commit()

  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.guild:
      return
    if not message.author.bot:
      c.execute("SELECT * FROM auto_channels WHERE channel_id=? AND tahwil=0", (message.channel.id,))
      data = c.fetchone()
      if data:
        url = data[1]
        tahwil = data[2]
        await message.channel.send(url)

    else:
      c.execute("SELECT * FROM auto_channels WHERE channel_id=? AND tahwil=1", (message.channel.id,))
      data = c.fetchone()
      if data and "has transferred" in message.content:
        url = data[1]
        await message.channel.send(url)

  @autoline.command(name="remove", description="stop the autoline in this channel")
  async def stop(self, inter: discord.Interaction):
    channel = inter.channel
    c.execute("SELECT * FROM auto_channels WHERE channel_id=?",(channel.id,))
    data = c.fetchone()
    if data:
      c.execute("DELETE FROM auto_channels WHERE channel_id=?",(channel.id,))
      conn.commit()
      await inter.response.send_message("autoline stopped in this channel", ephemeral=True)

    else:
      await inter.response.send_message("no autoline service in this channel", ephemeral=True)


async def setup(bot):
  await bot.add_cog(autoline(bot))