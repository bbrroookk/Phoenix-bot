import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import humanfriendly
import time as pytime
from datetime import datetime
import random
import sqlite3
import json

conn = sqlite3.connect('cmds/givs/giv.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS giv (msg_id INTEGER, channel INTEGER, endtime INTEGER, prize TEXT, button INTEGER, winners INTEGER, users TEXT)")
conn.commit()

emo = "🎉"
class Done(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label='this giveaway ended', style=discord.ButtonStyle.primary, custom_id="done", disabled=True)
  async def done(self, inter: discord.Interaction, button: discord.ui.Button):
    return

class Join(discord.ui.View):
  def __init__(self, users=None, *args, **kwargs):
    super().__init__(*args, **kwargs, timeout=None)
    self.users = users or []

  @discord.ui.button(label='', style=discord.ButtonStyle.secondary, custom_id="join", emoji=emo)
  async def join(self, inter: discord.Interaction, button: discord.ui.Button):
    if inter.user in self.users:
      await inter.response.send_message("You have already enered this giveaway!", ephemeral=True)
    else:
      self.users.append(inter.user)
      c.execute("UPDATE giv SET users=? WHERE channel=? AND msg_id=?", (json.dumps([u.id for u in self.users]), inter.channel.id, inter.message.id))
      conn.commit()
      await inter.response.send_message("You have enered this giveaway!", ephemeral=True)
      em = inter.message.embeds[0]
      em.set_field_at(0, name='Entries', value=str(len(self.users)), inline=False)
      await inter.message.edit(embed=em)

class Giv(commands.Cog):
  def __init__(self, bot,  *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bot = bot
    self.persistent_views_added = False

  async def end(self, channel_id, msg_id, endtime, prize, button, winners):
    channel = self.bot.get_channel(channel_id)
    msg = await channel.fetch_message(msg_id)
    em = msg.embeds[0]
    time = endtime - pytime.time()

    if time > 0:
      if button:
        c.execute("SELECT users FROM giv WHERE channel=? AND msg_id=?", (channel.id, msg.id))
        users_json = c.fetchone()[0]
        users = [await self.bot.fetch_user(user_id) for user_id in json.loads(users_json)]
        view = Join(users)
        await msg.edit(view=view)
        await asyncio.sleep(time)
        entries = view.users
        if len(entries) < winners:
          winners = len(entries)
        selected_winners = random.sample(entries, winners)
        em.set_field_at(0, name='Entries', value=str(len(entries)), inline=True)
        await msg.edit(embed=em)
      else:

        await msg.add_reaction(emo)
        await asyncio.sleep(time)
        msg = await channel.fetch_message(msg_id)
        reaction = next((r for r in msg.reactions if str(r.emoji) == emo), None)
        if reaction:
          users = []
          async for user in reaction.users():
            if not user.bot:
              users.append(user)

          winners_list = random.sample(users, min(winners, len(users)))
          selected_winners = winners_list
          entries = users
        else:
          selected_winners = []
          users = []

    else:
      if button:
        c.execute("SELECT users FROM giv WHERE channel=? AND msg_id=?", (channel.id, msg.id))
        users_json = c.fetchone()[0]
        users = [await self.bot.fetch_user(user_id) for user_id in json.loads(users_json)]
        entries = users

      else:
        msg = await channel.fetch_message(msg_id)
        reaction = next((r for r in msg.reactions if str(r.emoji) == emo), None)
        users = []

        if reaction:

          async for user in reaction.users():
            if not user.bot:
              users.append(user)
          entries = users
        else:
          entries = []

      if len(entries) < winners:
        winners = len(entries)
      selected_winners = random.sample(entries, winners)  

    if button:
      view = Done()
    else:
      view = None
    if selected_winners:
      try:
        winner = ', '.join(w.mention for w in selected_winners)
        em.description += f"\nWinners: {winner}"
        await msg.reply(f"{emo}Congratulation {winner}, you won the **`{prize}`**{emo}")
        await msg.edit(embed=em, view=view)
      except Exception as e:
        await channel.guild.owner.send(e)
    else:
      try:
        em.description += "\nNo winners"
        await msg.reply("Noe one entered the giveaway")
        await msg.edit(embed=em, view=view)
      except Exception as e:
        await channel.guild.owner.send(e)

    c.execute("DELETE FROM giv WHERE msg_id=? AND channel=?", (msg.id, channel.id))
    conn.commit()
    print(f"end method called for giveaway {msg_id}")

  giveaway = app_commands.Group(name='giveaway', description='set giveaway')

  @giveaway.command(name='create', description='start a giveaway')
  @app_commands.describe(duration="make sure to set useful units (ex: 5s, 3m, 4h, 5d, 8y...)", prize="type any prize", channel="where you want ur giveaway to start in?", button="if true : the giveaway will be with button", winners="number of winners", content="the content of giveaway message, you can mention here", image="must be an url")
  async def giv(self, inter: discord.Interaction, duration: str, prize: str, channel: discord.TextChannel=None, button: bool=False, winners: int=1, content: str=None, image: str=None):
    if not inter.user.guild_permissions.administrator:
      await inter.response.send_message("Sorry, you can't create giveaways, you must have administrator to do that", ephemeral=True)
      return
    try:  
      time = humanfriendly.parse_timespan(duration)
    except ValueError as e:
      await inter.response.send_message("The useful units are : s, m, h, d, y")
      return

    endtime = int(pytime.time() + time)
    if channel is None:
      channel = inter.channel

    em = discord.Embed(title=f"**{prize}**", url=f"https://discord.com/channels/{inter.guild.id}/{channel.id}", description=f"  - React with {emo} to join\n- Ends: <t:{endtime}:R> \n- by {inter.user.mention}", color=0xffffff)
    em.set_footer(text=f"{winners} winner(s)")
    em.set_thumbnail(url=inter.guild.icon.url)
    if button is True:
      em.add_field(name='Entries', value='0', inline=True)

    em.timestamp = datetime.utcnow()
    if image:
      em.set_image(url=image)
    else:
      em.set_image(url="https://media.discordapp.net/attachments/1141918453666685029/1141918535212343438/giveaways.jpg")

    if content:
      msg = await channel.send(content=content, embed=em)
    else:
      msg = await channel.send(content="**🎉GIVEAWAY START🎉**", embed=em)

    c.execute("INSERT INTO giv VALUES (?,?,?,?,?,?,?)", (msg.id, channel.id, endtime, prize, button, winners, json.dumps([])))
    conn.commit()
    await inter.response.send_message(f"Your giveaway has been sent too {channel.mention}", ephemeral=True)
    await Giv.end(self, channel.id, msg.id, endtime, prize, button, winners)


  @commands.Cog.listener()
  async def on_ready(self):
    if not self.persistent_views_added:
      self.bot.add_view(Join())
      self.persistent_views_added = True
    print("on_ready method called")
    c.execute("SELECT * FROM giv")
    giveaways = c.fetchall()
    for giveaway in giveaways:
      msg_id, channel_id, endtime, prize, button, winners, users = giveaway
      await Giv.end(self, channel_id, msg_id, endtime, prize, button, winners)



async def setup(bot):
  await bot.add_cog(Giv(bot))