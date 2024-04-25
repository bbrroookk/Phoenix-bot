import discord
from discord import app_commands
from discord.ext import commands



class muteClass(commands.Cog):
  def __init__(self, bot):
     self.bot = bot

  @commands.hybrid_command(name="mute", description="mute a user")
  async def mute_cmd(self, ctx, member: discord.Member):
    if not ctx.author.guild_permissions.administrator:
      return

    if member.bot:
      await ctx.send("u cant mute bots")
      return
    else:
      # check if the mentioned user's role is higher than the bot's role
      if member.top_role > ctx.me.top_role:
        await ctx.send("I can't mute this user as their role is higher than mine.")
        return

      muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
      if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for ch in ctx.guild.channels:
          await ch.set_permissions(muted_role, send_messages=False)

      if muted_role in member.roles:
        await ctx.reply(f'{member.mention} is already muted.')
      else:
        await member.add_roles(muted_role)
        await ctx.reply(f'{member.mention} has been muted.')



  @mute_cmd.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.reply(f"please use a valid format:\n- {prefix}mute @user")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f"Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply(f"An error occurred while executing the command: {error.original}")

  @commands.hybrid_command(name="unmute", description="unmute a user")
  async def unmute_cmd(self, ctx, member: discord.Member):
    if not ctx.author.guild_permissions.administrator:
      return


    if member.bot:
      await ctx.send("**u cant mute bots**")
      return
    else:
      # check if the mentioned user's role is higher than the bot's role
      if member.top_role > ctx.me.top_role:
        await ctx.send("I can't unmute this user as their role is higher than mine.")
        return

      muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
      if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for ch in ctx.guild.channels:
          await ch.set_permissions(muted_role, send_messages=False)

      if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.reply(f'{member.mention} has been unmuted.')
      else:
        await ctx.reply(f'{member.mention} is not muted.')

  @unmute_cmd.error
  async def unmute_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.reply(f"please use a valid format:\n- {prefix}unmute @user")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f"Missing argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply(f"An error occurred while executing the command: {error.original}")

  @commands.hybrid_command(name="mute_list", description="see a list of muted members")
  async def list(self, ctx):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role is None:
      em = discord.Embed(title="**Muted List**", description="there are no muted members.", colour=discord.Colour.red())
      await ctx.send(embed=em)
      return

    muted_members = [member.mention for member in ctx.guild.members if muted_role in member.roles]
    if not muted_members:
      em = discord.Embed(title="**Muted List**", description="there are no muted members.", colour=discord.Colour.red())
      em.set_footer(text=f'by {ctx.author.name}', icon_url=ctx.author.avatar.url)
      await ctx.send(embed=em)

    else:
      em = discord.Embed(title="**Muted List**", description="\n- "+"\n\n- ".join(muted_members), colour=discord.Colour.green())
      await ctx.send(embed=em)

async def setup(bot):
  await bot.add_cog(muteClass(bot))
