"""
BuildABot ExtraCode - Supermarket

Recognises codes from `./BuildABot/BuildABot/misc/bots/lines/supermarket.json`.
"""

import discord
import json
import typing
import discord_slash as interactions
import sussy
import random
import asyncpg
from discord.ext import commands

with open("./postgres.json") as postgresfile:
    postgres = json.load(postgresfile)
with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
    embed = json.load(embedfile)
with open("./BuildABot/BuildABot/misc/bab/lines/flameyfacts.json") as flameyfile:
    flameyfacts = json.load(flameyfile)

async def message(ctx: typing.Union[commands.Context, interactions.SlashContext], bot: commands.Bot, code: str):
    """Executes a Supermarket Code of `M` type."""

    code = code.split("+")
    codex = code[0].split("*")

    if codex[0] == "user":
        if code[1] == "amogass":
            await ctx.author.send(f"{sussy.twerk}")
        elif code[1] == "ff":
            factint = random.randint(0, 4)
            fact = flameyfacts[str(factint)]
            await ctx.send(f"**Flamey Fact #{factint + 1}:**\n{fact}")
        elif code[1] == "whensus":
            await ctx.author.send(f"{sussy.whensus}")
        elif code[1] == "amogus":
            await ctx.author.send(f"{sussy.amogus}")
    elif codex[0] == "dev":
        if code[1] == "cert":
            flamey = bot.get_user(450678229192278036)
            if codex[1] == "command":
                e = discord.Embed(title="New Command Request", color=int(embed["color"], 16), description="Someone got a Command from the Supermarket!")
            if codex[1] == "roast":
                e = discord.Embed(title="New Roast Request", color=int(embed["color"], 16), description="Someone got a Roast from the Supermarket!")
            e.set_author(name=embed["author"] + "Supermarket ExtraCode", icon_url=embed["icon"])
            e.add_field(name="The User", value=f"**Username:** {str(ctx.author)}\n**ID:** {ctx.author.id}")
            e.set_footer(text=embed["footer"], icon_url=embed["icon"])
            await flamey.send(content="I am a **BuildABot** bot, and I have a message!", embed=e)

async def run(ctx: typing.Union[commands.Context, interactions.SlashContext], bot: commands.Bot, command: str):
    """Executes a Supermarket Code of `R` type."""

    command: commands.Command = bot.get_command(command)
    await command.__call__(ctx.author)

async def database(ctx: typing.Union[commands.Context, interactions.SlashContext], bot: commands.Bot, code: str):
    """Executes a Supermarket Code of `DB` type."""

    async def execute(sql: str, stuff: str=None):
        db: asyncpg.Connection = await asyncpg.connect(postgres["buildabot"])
        if stuff is None:
            await db.execute(f'''{sql}''')
        else:
            await db.execute(f'''{sql}''', stuff)
    
    code = code.split("@")
    codex = code[0].split("*")

    if code[1] == "updates":
        await execute("INSERT INTO bab(updates) VALUES ($1)", ctx.author)
    elif code[1] == "plus":
        await execute("INSERT INTO bab(plus) VALUES ($1)", bot.user.id)