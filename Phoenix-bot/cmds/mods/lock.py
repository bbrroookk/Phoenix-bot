import discord
from discord import app_commands
from discord.ext import commands
import sqlite3



class lock(commands.Cog):
  def __init__(self, bot):
     self.bot = bot

  @commands.hybrid_command(name="lock", description="lock a channel")
  async def lock(self, ctx, channel: discord.TextChannel=None):
    if not ctx.author.guild_permissions.administrator:
        return

    # check if the bot has the required permissions
    if not ctx.guild.me.guild_permissions.manage_channels:
        await ctx.send("I don't have the required permissions to lock a channel.")
        return

    if not channel:
      channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is False:
      await ctx.reply(f'{channel.mention} is already locked')
    else:
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.reply(f'**{channel.mention} has been locked**')

  @lock.error
  async def lock_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send(f"please use a valid format:\n- {prefix}lock\n- {prefix}lock #channel")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f"Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply(f"An error occurred while executing the command: {error.original}")


  @commands.hybrid_command(name="unlock", description="unlock a channel")
  async def unlock(self, ctx, channel: discord.TextChannel=None):
    if not ctx.author.guild_permissions.administrator:
      return

    # check if the bot has the required permissions
    if not ctx.guild.me.guild_permissions.manage_channels:
        await ctx.send("I don't have the required permissions to unlock a channel.")
        return

    if not channel:
      channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is True:
      await ctx.reply(f'{channel.mention} is not locked')
    else:
      overwrite.send_messages = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.reply(f'**{channel.mention} has been unlocked**')

  @unlock.error
  async def unlock_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send(f"please use a valid format:\n- {prefix}unlock\n- {prefix}unlock #channel")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f"Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply(f"An error occurred while executing the command: {error.original}")



async def setup(bot):
  await bot.add_cog(lock(bot))
