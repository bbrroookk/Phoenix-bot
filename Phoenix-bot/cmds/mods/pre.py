import discord
from discord.ext import commands
import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="prefix", description="change the bot's prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str):
        with open("data/prefix.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open("data/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"The bot's prefix has been changed to `{new_prefix}`")

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need to have administrator permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument: {error.param.name}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
      with open("data/prefix.json", "r") as f:
        prefixes = json.load(f)

      prefixes[str(guild.id)] = "$"

      with open("data/prefix.json", "w") as f:
        json.dump(prefixes, f, indent=4)

def p(client, message):
    with open("data/prefix.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

async def setup(bot):
    await bot.add_cog(Prefix(bot))
