import discord
import discord_slash as interactions
import tracemalloc
import json
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("bab ", "BAB ", "Bab "), intents=discord.Intents.all())
slash = interactions.SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, override_type=True)

tracemalloc.start()

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)
with open("./BuildABot/BuildABot/assets/embed.json") as embedfile:
    embed = json.load(embedfile)

@bot.event
async def on_ready():
    channel: discord.TextChannel = bot.get_channel(863150083913416748)
    await channel.send(f"BuildABot is ready and running on discord.py v{discord.__version__}!")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    e = discord.Embed(title="An Error Occurred", color=int(embed["color"], 16), description=f"{error}")
    e.set_author(name=embed["author"], icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

    raise error

@bot.event
async def on_slash_command_error(ctx: interactions.SlashContext, ex):
    e = discord.Embed(title="An Error Occurred", color=int(embed["color"], 16), description=f"{ex}")
    e.set_author(name=embed["author"], icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

    raise ex

extensions = ["cogs.botmanager", "cogs.core", "jishaku"]
for extension in extensions:
    bot.load_extension(extension)

bot.run(token["bab"]["bot"])