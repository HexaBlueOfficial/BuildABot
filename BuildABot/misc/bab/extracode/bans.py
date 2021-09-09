"""
BuildABot ExtraCode - Bans

BuildABot banning functions.
"""

import discord
import json
from discord.ext import commands

with open("./bans.json") as bansfile:
    bans = json.load(bansfile)
with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
    embed = json.load(embedfile)

def check(ctx: commands.Context):
    for ban in bans["bab"]:
        if ban[0] == ctx.author.id:
            return True
        else:
            return False

async def banned(ctx: commands.Context):
    daysbanned = "[NOT FOUND]"
    for ban in bans["bab"]:
        if ban[0] == ctx.author.id:
            daysbanned = ban[1]
            break
    
    if daysbanned is None:
        daysbanned = "∞"

    e = discord.Embed(title="You're Banned", color=int(embed["nocolor"], 16), description=f"We're sorry. It looks like one member of **HexaCode**'s Team (BuildABot's Developers) has **banned you from using BuildABot and all Bots made with it** for {daysbanned} days.")
    e.set_author(name=embed["author"] + "Bans ExtraCode", icon_url=embed["icon"])
    e.set_thumbnail(url=embed["noicon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

async def ban(ctx: commands.Context, user: int, days: int=None):
    bans["bab"].append([user, days])

    with open("./bans.json", "w") as bansfile:
        json.dump(bans, bansfile)
    
    user = await ctx.bot.fetch_user(user)

    if days is None:
        days = "∞"
    
    e = discord.Embed(title="Ban Successful", color=int(embed["color"], 16), description=f"Successfully banned {user.name} from using **BuildABot** and **all Bots made with BuildABot** for {days} days.")
    e.set_author(name=embed["author"] + "Bans ExtraCode", icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

async def unban(ctx: commands.Context, user: int):
    banlist: list = bans["bab"]
    
    for ban in banlist:
        if ban[0] == user:
            banlist.remove(ban)
            break

    with open("./bans.json", "w") as bansfile:
        json.dump(bans, bansfile)
    
    user = await ctx.bot.fetch_user(user)
    
    e = discord.Embed(title="Unban Successful", color=int(embed["color"], 16), description=f"Successfully banned {user.name} from using **BuildABot** and **all bots made with BuildABot**.")
    e.set_author(name=embed["author"] + "Bans ExtraCode", icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)