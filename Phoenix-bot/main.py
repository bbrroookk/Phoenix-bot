import discord
from discord import app_commands
from discord.ext import commands
import os
import sys
sys.path.append('cmds/mods')
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="*", intents=discord.Intents.all())
tree = bot.tree

async def load():
  for root, dirs, files in os.walk('cmds'):
    for fn in files:
      if fn.endswith('.py'):
        path = os.path.join(root, fn).replace("/", ".")[:-3]
        try:
          await bot.load_extension(path)
          print(f'Loaded {path}')
        except Exception as e:
          print(e)

@bot.event
async def on_ready():

  print(f'logged as {bot.user} ')
  await load()
  await tree.sync()
  for cog_name, cog_instance in bot.cogs.items():
        # Check if the cog has a method with the name of the cog followed by '_on_ready'
        method_name = f'{cog_name}_on_ready'
        if hasattr(cog_instance, method_name):
            # Get the method and call it
            method = getattr(cog_instance, method_name)
            await method()

keep_alive()

try:
    bot.run(os.environ['Token'])
except discord.errors.HTTPException:
    os.system("kill 1")
    os.system("python main.py")