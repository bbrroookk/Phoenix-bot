import discord
from discord import app_commands
from discord.ext import commands


class msg(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name="say", description="send a msg using this bot")
  async def say(self, inter: discord.Interaction, message: str):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message(f"u can't do that hahahah", ephemeral=True)
      return

    await inter.channel.send(message)
    await inter.response.send_message("done", ephemeral=True)


  @app_commands.command(name="embed", description="send embed using this bot")
  @app_commands.choices(color=[
    discord.app_commands.Choice(name="black", value=0x000000),
    discord.app_commands.Choice(name="white", value=0xEFEFEF),
    discord.app_commands.Choice(name="red", value=0xFF0000),
    discord.app_commands.Choice(name="green", value=0x00FF00),
    discord.app_commands.Choice(name="blue", value=0x205375),
    discord.app_commands.Choice(name="yellow", value=0xFFFF00),
    discord.app_commands.Choice(name="magenta", value=0xFF00FF),
    discord.app_commands.Choice(name="cyan", value=0x00FFFF),
    discord.app_commands.Choice(name="orange", value=0xF66B0E),
    discord.app_commands.Choice(name="purple", value=0x800080),
    discord.app_commands.Choice(name="pink", value=0xE806FF),
    discord.app_commands.Choice(name="brown", value=0xA52A2A),
    discord.app_commands.Choice(name="gray", value=0x808080),
    discord.app_commands.Choice(name="dark red", value=0x8B0000),
    discord.app_commands.Choice(name="dark green", value=0x006400),
    discord.app_commands.Choice(name="dark blue", value=0x112B3C),
    discord.app_commands.Choice(name="gold", value=0xFFD700),
    discord.app_commands.Choice(name="silver", value=0xC0C0C0),
    discord.app_commands.Choice(name="bronze", value=0xCD7F32),
    discord.app_commands.Choice(name="navy blue", value=0x000080),
    discord.app_commands.Choice(name="olive green", value=0x808000),
    discord.app_commands.Choice(name="lime green", value=0x32CD32),
    discord.app_commands.Choice(name="teal blue", value=0x008080),
    discord.app_commands.Choice(name="indigo blue", value=0x4B0082)
],author_icon=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
],thumbnail=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
],footer_icon=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
])
  @app_commands.describe(channel='اين تريد ارسال الامبد', content="الرسالة التي خارج الامبد حيث يمكن المنشن", title="عنوان الامبد", description="الوصف و هو محتوى الامبد", color="اختر لون من القائمة", image="الصورة الكبيرة في الامبد ،يجب ان يكون رابط", author="صاحب الامبد ؛الكتابة فوق العنوان", author_icon="الصورة الصغيرة اللي تجي فوق العنوان ", thumbnail="الصورة المقابلة للعنوان", footer="الكتابة التي تكون اسفل الامبد", footer_icon="اختر صورة", add_time="هل تريد اضافة وقت ارسال الامبد؟")

  async def embed(self, inter: discord.Interaction, channel: discord.TextChannel=None, content: str=None, title: str=None, description: str=None, color: discord.app_commands.Choice[int]=None, image: str=None, author: str=None, author_icon: discord.app_commands.Choice[int]=None, thumbnail:  discord.app_commands.Choice[int]=None, footer: str=None, footer_icon:  discord.app_commands.Choice[int]=None, add_time: bool=False):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("u can't send the embed , you are not an admin", ephemeral=True)
      return

    if all(arg is None for arg in [channel, content, title, description, color, image, author, author_icon, thumbnail, footer, footer_icon]):
        await inter.response.send_message("You didn't select anything", ephemeral=True)
        return              

    if channel is None:
      channel = inter.channel

    if color:
      color = color.value
    else:
      color = 0x99aab5

    em = discord.Embed(title=title, description=description, color=color)

    if image:
      em.set_image(url=image)
    if author:
      if author_icon:
        if author_icon.value == 1:
          author_icon = inter.guild.icon.url
        elif author_icon.value == 2:
          author_icon = inter.user.display_avatar
        else:
          author_icon = None

        em.set_author(name=author, icon_url=author_icon)

    if thumbnail:
        if thumbnail.value == 1:
          thumbnail = inter.guild.icon.url
        elif thumbnail.value == 2:
          thumbnail = inter.user.display_avatar
        else:
          thumbnail = None

        em.set_thumbnail(url=thumbnail)

    if footer:
      if footer_icon:
        if footer_icon.value == 1:
          footer_icon = inter.guild.icon.url
        elif footer_icon.value == 2:
          footer_icon = inter.user.display_avatar
        else:
          footer_icon = None

      em.set_footer(text=footer, icon_url=footer_icon)

    await channel.send(content=content, embed=em)
    await inter.response.send_message(f'your embed sent to {channel.mention} ', ephemeral=True)


  @app_commands.command(name="edit_message", description="edit a message")
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
    discord.app_commands.Choice(name="pink", value=0xE806FF),
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
    discord.app_commands.Choice(name="indigo blue", value=0x4B0082)
],author_icon=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
],thumbnail=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
],footer_icon=[
    discord.app_commands.Choice(name="server icon", value=1),
    discord.app_commands.Choice(name="your avatar", value=2)
])
  @app_commands.describe(message_id="ايدي الرسالة اللي تريد تعديلها",channel='اين هي  الامبد', content="الرسالة التي خارج الامبد حيث يمكن المنشن", title="عنوان الامبد", description="الوصف و هو محتوى الامبد", color="اختر لون من القائمة", image="الصورة الكبيرة في الامبد ،يجب ان يكون رابط", author="صاحب الامبد ؛الكتابة فوق العنوان", author_icon="الصورة الصغيرة اللي تجي فوق العنوان ", thumbnail="الصورة المقابلة للعنوان", footer="الكتابة التي تكون اسفل الامبد", footer_icon="اختر صورة", add_time="هل تريد اضافة وقت ارسال الامبد؟")

  async def edit(self, inter: discord.Interaction, message_id: str, channel: discord.TextChannel, content: str=None, title: str=None, description: str=None, color: discord.app_commands.Choice[int]=None, image: str=None, author: str=None, author_icon: discord.app_commands.Choice[int]=None, thumbnail:  discord.app_commands.Choice[int]=None, footer: str=None, footer_icon:  discord.app_commands.Choice[int]=None, add_time: bool=False):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("u can't send the embed , you are not an admin", ephemeral=True)
      return

    try:
      message = await channel.fetch_message(message_id)
    except discord.NotFound:
      await inter.response.send_message(f"message not found in {channel.mention}, make sure u select the right channel or check ur message id ", ephemeral=True)
      return

    if not message.embeds:
      await message.edit(content=content)
      await inter.response.send_message("ur msg don't contain any embeds , i just edit the content", ephemeral=True)
      return

    em = message.embeds[0]

    if title:
      em.title = title

    if description:
      em.description = description

    if color:
      color = color.value
      em.color = color

    if image:
      em.set_image(url=image)
    if author:
      if author_icon:
        if author_icon.value == 1:
          author_icon = inter.guild.icon.url
        elif author_icon.value == 2:
          author_icon = inter.user.display_avatar
        else:
          author_icon = None

        em.set_author(name=author, icon_url=author_icon)

    if thumbnail:
        if thumbnail.value == 1:
          thumbnail = inter.guild.icon.url
        elif thumbnail.value == 2:
          thumbnail = inter.user.display_avatar
        else:
          thumbnail = None

        em.set_thumbnail(url=thumbnail)

    if footer:
      if footer_icon:
        if footer_icon.value == 1:
          footer_icon = inter.guild.icon.url
        elif footer_icon.value == 2:
          footer_icon = inter.user.display_avatar
        else:
          footer_icon = None

      em.set_footer(text=footer, icon_url=footer_icon)

    await message.edit(content=content, embed=em)
    await inter.response.send_message(f'your message has been edited ', ephemeral=True)






async def setup(bot):
  await bot.add_cog(msg(bot))