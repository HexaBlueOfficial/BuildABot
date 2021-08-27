"""
BuildABot ExtraCode - BanCheck

Checks for a BuildABot Ban.
"""

import discord
import json
from discord.ext import commands

with open("./BuildABot/BuildABot/misc/bab/assets/bans.json") as bansfile:
    bans = json.load(bansfile)
with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
    embed = json.load(embedfile)

def check(ctx: commands.Context):
    if ctx.author.id in bans["bans"]:
        return True
    else:
        return False

async def banned(ctx: commands.Context):
    timebanned = "?"
    for ban in bans["bans"]:
        if ban[0] == ctx.author.id:
            timebanned = ban[1]
            break

    e = discord.Embed(title="You're Banned", color=int(embed["nocolor"], 16), description=f"We're sorry. It looks like one member of **HexaCode**'s Team (BuildABot's Developers) has **banned you from using BuildABot and all Bots made with it** for {timebanned} days.")
    e.set_author(name=embed["author"] + "BanCheck ExtraCode", icon_url=embed["icon"])
    e.set_thumbnail(url=embed["noicon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)