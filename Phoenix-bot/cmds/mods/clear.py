import discord
from discord import app_commands
from discord.ext import commands
from asyncio import sleep



class clear(commands.Cog):
  def __init__(self, bot):
     self.bot = bot

  @commands.hybrid_command(name="clear", description="purge messages in this channel", aliases=["purge"])
  async def clear(self, ctx, amount: int, user: discord.Member=None):
    if not ctx.author.guild_permissions.administrator:
      return

    # check if the bot has the required permissions
    if not ctx.guild.me.guild_permissions.manage_messages:
        await ctx.send("I don't have the required permissions to delete messages.")
        return

    if user and not ctx.guild.get_member(user.id):
      msg = await ctx.send("Sorry, I can't find this user in this server")
      await  ctx.message.delete()
      await sleep(5)
      await msg.delete()

    ch = ctx.channel
    def check(m):
      return (m.author == user) if user else True
    await ctx.message.delete()
    msg = await ctx.send("**Deleting messages...**")
    await ctx.channel.purge(limit=amount +1, check=check)
    if msg:
      await msg.delete()
    message = await ch.send(f"**Cleared {amount} messages in this channel**")
    await sleep(2)
    await message.delete()





  @clear.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.reply(f"please use a valid format:\n- {prefix}clear [amount] (must be number).\n- {prefix}clear [amount] @user (to clear messages by this user only) ")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f"Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply(f"An error occurred while executing the command: {error.original}")

async def setup(bot):
  await bot.add_cog(clear(bot))
