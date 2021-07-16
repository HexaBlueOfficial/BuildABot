import discord
import json
import asyncpg
import discord_slash as interactions
from discord_slash import cog_ext
from discord.ext import commands

class Core(commands.Cog):
    """Core commands, like a Info command or... an Easter Egg?"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    async def pgselect(self, query: str):
        db: asyncpg.Connection = asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    @commands.command(name="info")
    async def info(self, ctx: commands.Context):
        """Get info about the Bot."""

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        featuredescriber = ""
        if bot[4] == "core:help":
            featuredescriber = "fairly useless"
        elif bot[4] == "core:help:fun":
            featuredescriber = "fun"
        elif bot[4] == "core:help:utility":
            featuredescriber = "utilitarian"
        elif bot[4] == "core:help:moderation":
            featuredescriber = "moderation"
        else:
            featuredescriber = "multifunctional"
        
        e = discord.Embed(title=f"About {bot[5]}", color=int(bot[7], 16), description=f"**{bot[5]}** is a **{featuredescriber} Bot** created off of **BuildABot** by **Earth Development**.\nBot created in the {self.bot.get_guild(bot[0]).name} server.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Core", icon_url=bot[6])
        e.set_footer(name=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e, components=[
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "What is BuildABot?", None, None, "https://discord.gg/bacZt25ZGZ")
            )
        ])
    
    @cog_ext.cog_slash(name="info", description="Core - Get info about the Bot.")
    async def _info(self, ctx: interactions.SlashContext):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        featuredescriber = ""
        if bot[4] == "core:help":
            featuredescriber = "fairly useless"
        elif bot[4] == "core:help:fun":
            featuredescriber = "fun"
        elif bot[4] == "core:help:utility":
            featuredescriber = "utilitarian"
        elif bot[4] == "core:help:moderation":
            featuredescriber = "moderation"
        else:
            featuredescriber = "multifunctional"
        
        e = discord.Embed(title=f"About {bot[5]}", color=int(bot[7], 16), description=f"**{bot[5]}** is a **{featuredescriber} Bot** created off of **BuildABot** by **Earth Development**.\nBot created in the {self.bot.get_guild(bot[0]).name} server.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Core", icon_url=bot[6])
        e.set_footer(name=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e, components=[
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "What is BuildABot?", None, None, "https://discord.gg/bacZt25ZGZ")
            )
        ])
    
    @commands.command(name="bab", hidden=True)
    async def bab(self, ctx: commands.Context):
        """???"""

        await ctx.send("**Flamey** (developer of **BuildABot**) always puts a prefix-based Easter Egg in his bots. But this time... he didn't know what to do, because he can't predict prefixes!\nSo he did this. Nice find.")

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))