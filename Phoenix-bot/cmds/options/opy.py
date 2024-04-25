import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
from asyncio import sleep

conn = sqlite3.connect("data/data.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS wlcm (category_id INTEGER, title TEXT, descreption Text, color INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS opts (category_id INTEGER, name TEXT, description TEXT, emoji TEXT, message TEXT, embed TEXT)")
conn.commit()

class MySelect(discord.ui.Select):
  def __init__(self, category_id: int=None):
    c.execute("SELECT name, description, emoji FROM opts WHERE category_id=?", (category_id,))
    opts = [discord.SelectOption(label=row[0], description=row[1], value=row[0], emoji=row[2]) for row in c.fetchall()]

    super().__init__(placeholder="choose your order",min_values=1,max_values=1, options=opts, custom_id='select')

  async def callback(self, inter: discord.Interaction):
    c.execute("SELECT message, embed FROM opts WHERE category_id=? AND name=?", (inter.channel.category.id, self.values[0]))
    data = c.fetchone()
    if data:
      message, embed_description = data
      if message and embed_description:
        em = discord.Embed(description=embed_description, colour= discord.Colour.random())
        try:
          await inter.response.send_message(content=message, embed=em, allowed_mentions=discord.AllowedMentions(everyone=True))
          await inter.channel.edit(name=f'{self.values[0]}')
        except Exception as e:
          await inter.guild.owner.send(e)

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MySelect())



class Options(commands.Cog):
  def __init__(self, bot):
     self.bot = bot
     self.persistent_views_added = False

  @commands.Cog.listener()
  async def on_ready(self):
    if not self.persistent_views_added:
      self.bot.add_view(MyView())
      self.persistent_views_added = True

  options = app_commands.Group(name='options', description='set options')

  @options.command(name="setup", description="setup the options message")
  @app_commands.choices(color=[
    discord.app_commands.Choice(name="black", value=0x000000),
    discord.app_commands.Choice(name="white", value=0xFFFFFF),
    discord.app_commands.Choice(name="red", value=0xFF0000),
    discord.app_commands.Choice(name="green", value=0x00FF00),
    discord.app_commands.Choice(name="blue", value=0x0000FF),
    discord.app_commands.Choice(name="yellow", value=0xFFFF00),
    discord.app_commands.Choice(name="magenta", value=0xFF00FF),
    discord.app_commands.Choice(name="cyan", value=0x00FFFF),
    discord.app_commands.Choice(name="orange", value=0xFFA500),
    discord.app_commands.Choice(name="purple", value=0x800080),
    discord.app_commands.Choice(name="pink", value=0xFFC0CB),
    discord.app_commands.Choice(name="brown", value=0xA52A2A),
    discord.app_commands.Choice(name="gray", value=0x808080),
    discord.app_commands.Choice(name="dark red", value=0x8B0000),
    discord.app_commands.Choice(name="dark green", value=0x006400),
    discord.app_commands.Choice(name="dark blue", value=0x00008B),
    discord.app_commands.Choice(name="gold", value=0xFFD700),
    discord.app_commands.Choice(name="silver", value=0xC0C0C0),
    discord.app_commands.Choice(name="bronze", value=0xCD7F32),
    discord.app_commands.Choice(name="navy blue", value=0x000080),
    discord.app_commands.Choice(name="olive green", value=0x808000),
    discord.app_commands.Choice(name="lime green", value=0x32CD32),
    discord.app_commands.Choice(name="teal blue", value=0x008080),
    discord.app_commands.Choice(name="indigo blue", value=0x4B0082)])
  @app_commands.describe(category="اختر كاتيغوري التكتات", title="عنوان الرسالة اللي تترسل مع فتح التكت", description="محتوى الرسالة", color="اختر لون بس")
  async def setup(self, inter: discord.Interaction, category: discord.CategoryChannel, title: str, description: str, color: discord.app_commands.Choice[int]):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("sorry, only admins can do that", ephemeral=True)
      return

    if not category or not isinstance(category, discord.CategoryChannel):
      await inter.response.send_message("Error: Invalid category ", ephemeral=True)
      return

    c.execute("INSERT OR REPLACE INTO wlcm VALUES (?,?,?,?)", (category.id, title, description, color.value))
    conn.commit()

    await inter.response.send_message(f"Successfully set to {category.name} ")


  @options.command(name="add", description="Add to the options message")
  @app_commands.describe(category="كاتيغوري التكتات", option_name="اسم الخيار", option_description="وصف الخيار", emoji="ايموجي الخيار، تأكد انه موجود في السيرفر و احرص على عدم حذفه او تغيير اسمه", reply_message="الرسالة اللي تترسل بعد اختيار هذا الخيار", reply_embed="الامبد المصاحبة للرسالة")
  async def add(self, inter: discord.Interaction, category: discord.CategoryChannel, option_name: str, option_description: str, emoji: str, reply_message: str, reply_embed: str):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("sorry, only admins can do that", ephemeral=True)
      return

    c.execute("INSERT OR IGNORE INTO opts VALUES (?,?,?,?,?,?)", (category.id, option_name, option_description, emoji, reply_message, reply_embed))
    conn.commit()
    await inter.response.send_message(f"added {option_name} option for {category.name}", ephemeral=True)


  @options.command(name="edit", description="edit an eption for the options message")
  async def edit(self, inter: discord.Interaction, category: discord.CategoryChannel, old_option_name: str, new_option_name: str, option_description: str=None, emoji: str=None, reply_message: str=None, reply_embed: str=None):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("sorry, only admins can do that", ephemeral=True)
      return

    c.execute("UPDATE opts SET name = COALESCE(?, name), desciption = COALESCE(?, desciption), emoji = COALESCE(?, emoji), message = COALESCE(?, message), embed = COALESCE(?, embed) WHERE category_id = ? AND name = ?", (new_option_name, option_description, emoji, reply_message, reply_embed, category.id, old_option_name))
    conn.commit()
    if c.rowcount > 0:
      await inter.response.send_message(f"Updated {old_option_name} option for {category.name}", ephemeral=True)
    else:
      await inter.response.send_message(f"Error: {old_option_name} option not found in  {category.name}", ephemeral=True)

  @options.command(name="remove", description="remove an eption from the options message")
  async def remove(self, inter: discord.Interaction, category: discord.CategoryChannel, option_name: str):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("sorry, only admins can do that", ephemeral=True)
      return

    c.execute("DELETE FROM opts WHERE category_id=? AND name=?", (category.id, option_name))
    conn.commit()
    if c.rowcount > 0:
      await inter.response.send_message(f"Removed {option_name} option from {category.name}", ephemeral=True)
    else:
      await inter.response.send_message(f"Error: {option_name} option not found in  {category.name}", ephemeral=True)

  @options.command(name='edit_welcome', description='Edit welcome message for category')
  @app_commands.choices(new_color=[
    discord.app_commands.Choice(name="black", value=0x000000),
    discord.app_commands.Choice(name="white", value=0xFFFFFF),
    discord.app_commands.Choice(name="red", value=0xFF0000),
    discord.app_commands.Choice(name="green", value=0x00FF00),
    discord.app_commands.Choice(name="blue", value=0x0000FF),
    discord.app_commands.Choice(name="yellow", value=0xFFFF00),
    discord.app_commands.Choice(name="magenta", value=0xFF00FF),
    discord.app_commands.Choice(name="cyan", value=0x00FFFF),
    discord.app_commands.Choice(name="orange", value=0xFFA500),
    discord.app_commands.Choice(name="purple", value=0x800080),
    discord.app_commands.Choice(name="pink", value=0xFFC0CB),
    discord.app_commands.Choice(name="brown", value=0xA52A2A),
    discord.app_commands.Choice(name="gray", value=0x808080),
    discord.app_commands.Choice(name="dark red", value=0x8B0000),
    discord.app_commands.Choice(name="dark green", value=0x006400),
    discord.app_commands.Choice(name="dark blue", value=0x00008B),
    discord.app_commands.Choice(name="gold", value=0xFFD700),
    discord.app_commands.Choice(name="silver", value=0xC0C0C0),
    discord.app_commands.Choice(name="bronze", value=0xCD7F32),
    discord.app_commands.Choice(name="navy blue", value=0x000080),
    discord.app_commands.Choice(name="olive green", value=0x808000),
    discord.app_commands.Choice(name="lime green", value=0x32CD32),
    discord.app_commands.Choice(name="teal blue", value=0x008080),
    discord.app_commands.Choice(name="indigo blue", value=0x4B0082)])
  async def edit_welcome(self, inter: discord.Interaction, category: discord.CategoryChannel, new_title: str, new_description: str, new_color: discord.app_commands.Choice[int]):
    if not inter.user.guild_permissions.administrator:
        await inter.response.send_message("Sorry, only admins can use this command", ephemeral=True)
        return
    if not category or not isinstance(category, discord.CategoryChannel):
        await inter.response.send_message("Error: Invalid category", ephemeral=True)
        return
    c.execute("SELECT * FROM wlcm WHERE category_id=?", (category.id,))
    data = c.fetchone()
    if not data:
        await inter.response.send_message(f"No welcome message found for category {category.name}", ephemeral=True)
        return
    c.execute("UPDATE wlcm SET title=?, descreption=?, color=? WHERE category_id=?", (new_title, new_description, new_color.value, category.id))
    conn.commit()
    await inter.response.send_message(f"Successfully updated welcome message for category {category.name}", ephemeral=True)

  @options.command(name="delete_welcome", description="Delete welcome message for category")
  async def delete_welcome(self, inter: discord.Interaction, category: discord.CategoryChannel):
    if not inter.user.guild_permissions.administrator:
        await inter.response.send_message("Sorry, only admins can use this command", ephemeral=True)
        return
    if not category or not isinstance(category, discord.CategoryChannel):
        await inter.response.send_message("Error: Invalid category", ephemeral=True)
        return
    c.execute("DELETE FROM wlcm WHERE category_id=?", (category.id,))
    conn.commit()
    await inter.response.send_message(f"Successfully deleted welcome message for category {category.name}", ephemeral=True)


  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    if channel.category and channel.name.startswith("ticket"):
      c.execute("SELECT * FROM wlcm WHERE category_id=?", (channel.category.id,))
      data = c.fetchone()
      if data:
        title , description, color = data[1], data[2], data[3]
        await sleep(2)
        em = discord.Embed(title=title, description=description, color=color)
        c.execute("SELECT COUNT(*) FROM opts WHERE category_id=?", (channel.category.id,))
        data = c.fetchone()[0]
        try:
          if data > 0:
            view = discord.ui.View()
            view.add_item(MySelect(channel.category.id))
            await channel.send(embed=em, view=view)
          else:
            await channel.send(embed=em)
        except Exception as e:
          await print(e)

async def setup(bot):
  await bot.add_cog(Options(bot))