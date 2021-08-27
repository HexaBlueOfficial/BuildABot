import discord
import json
import asyncpg
import typing
import discord_slash as interactions
from ..misc.bab.extracode import bancheck
from discord_slash import cog_ext
from discord.ext import commands

class Premium(commands.Cog):
    """Commands for the coolest of the coolest! The **BuildABot** supporters!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
    
    async def pgselect(self, query: str):
        db: asyncpg.Connection = asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')

def setup(bot: commands.Bot):
    bot.add_cog(Premium(bot))