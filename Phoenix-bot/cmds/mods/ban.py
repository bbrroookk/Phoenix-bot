import discord
from discord import app_commands
from discord.ext import commands


class KickBanClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="kick", description="kick a user")
    async def kick_cmd(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.administrator:
            return

        # check if the mentioned user's role is higher than the bot's role
        if member.top_role > ctx.me.top_role:
            await ctx.send("``` I can't kick this user as their role is higher than mine.```")
            return

        await member.kick()
        await ctx.reply(f'**🦵 | {member.mention} has been kicked.**')

    @kick_cmd.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply(embed = discord.Embed(title="please use a valid format:", description=f"- {prefix}kick @user."))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"```Missing argument: {error.param.name}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(f"```An error occurred while executing the command: {error.original}```")

    @commands.hybrid_command(name="ban", description="ban a user")
    async def ban_cmd(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.administrator:
            return

        # check if the mentioned user's role is higher than the bot's role
        if member.top_role > ctx.me.top_role:
            await ctx.send("```I can't ban this user as their role is higher than mine.```")
            return

        await member.ban()
        await ctx.reply(f'**✈️ | {member.mention} has been banned.**')

    @ban_cmd.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply(embed = discord.Embed(title="please use a valid format:", description=f"\n- {prefix}ban @user"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"```Missing argument: {error.param.name}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(f"```An error occurred while executing the command: {error.original}```")

    @commands.hybrid_command(name="unban", description="unban a user")
    async def unban_cmd(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.administrator:
            return

        # check if the mentioned user's role is higher than the bot's role
        if member.top_role > ctx.me.top_role:
            await ctx.send("```I can't unban this user as their role is higher than mine.```")
            return

        await member.unban()
        await ctx.reply(f'**{member.mention} has been unbanned.***')

    @unban_cmd.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply(embed = discord.Embed(title="please use a valid format:", description=f"\n- {prefix}unban @user"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"```Missing argument: {error.param.name}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(f"```An error occurred while executing the command: {error.original}```")

    @commands.hybrid_command(name="ban_list", description="see a list of banned members")
    async def list(self, ctx):
        banned_members = [entry.user.mention for entry in await ctx.guild.bans()]
        if not banned_members:
            em = discord.Embed(title="**Banned List**", description="there are no banned members.", colour=discord.Colour.red())
            em.set_footer(text=f'by {ctx.author.name}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="**Banned List**", description="\n- "+"\n\n- ".join(banned_members), colour=discord.Colour.green())
            await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(KickBanClass(bot))
