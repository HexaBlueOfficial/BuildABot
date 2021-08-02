import typing
import discord
import json
import asyncpg
import platform
import discord_slash as interactions
from datetime import datetime
from discord_slash import cog_ext
from discord.ext import commands

class Core(commands.Cog):
    """Core Commands, like a Info command or... an Easter Egg?"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    async def pgselect(self, query: str):
        db: asyncpg.Connection = asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()
    
    async def info(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        featuredescriber = ""
        if bot[4] == "core:help":
            featuredescriber = "fairly useless"
        elif bot[4] == "core:help:fun":
            featuredescriber = "fun"
        elif bot[4] == "core:help:utility":
            featuredescriber = "utilitarian"
        else:
            featuredescriber = "multifunctional"
        
        e = discord.Embed(title=f"About {bot[5]}", color=int(bot[7], 16), description=f"**{bot[5]}** is a **{featuredescriber} Bot** created off of **BuildABot** by **Earth Development**.\nBot created in the {self.bot.get_guild(bot[0]).name} server.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Core", icon_url=bot[6])
        e.set_thumbnail(url=bot[6])
        e.add_field(name="BuildABot Developers", value="<@450678229192278036>: All commands and their Slash equivalents.\n<@598325949808771083>: `bab help`.", inline=False)
        e.add_field(name="BuildABot Versions", value=f"BuildABot: v0.0.6\nPython: v{platform.python_version()}\ndiscord.py: v{discord.__version__}", inline=False)
        e.add_field(name="Credits", value="**Created with:** BuildABot", inline=False)
        e.set_image(url=self.embed["banner"])
        e.set_footer(name=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e, components=[
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "What is BuildABot?", None, None, "https://discord.gg/bacZt25ZGZ")
            )
        ])
    
    @commands.command(name="info")
    async def dpyinfo(self, ctx: commands.Context):
        """Get info about the Bot."""

        await self.info(ctx)
    
    @cog_ext.cog_subcommand(base="info", name="bot", description="Core - Get info about the Bot.")
    async def slashinfobot(self, ctx: interactions.SlashContext):
        await self.info(ctx)
    
    async def ping(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        ping = round(self.bot.latency * 1000, 1)

        e = discord.Embed(title="Ping Latency", color=int(bot[7], 16), description=f"My Ping Latency is {ping}ms.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Core", icon_url=bot[6])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="ping", aliases=["latency", "lat"])
    async def dpyping(self, ctx: commands.Context):
        """Gets the Bot's Ping Latency."""

        await self.ping(ctx)
    
    @cog_ext.cog_slash(name="ping", description="Core - Gets the Bot's Ping Latency.")
    async def slashping(self, ctx: interactions.SlashContext):
        await self.ping(ctx)
    
    async def uptime(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=int(bot[7], 16), description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Core", icon_url=bot[6])
        e.add_field(name="Last Restart", value="The Bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")))
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="uptime")
    async def dpyuptime(self, ctx: commands.Context):
        """Shows the Bot's Uptime."""

        await self.uptime(ctx)
    
    @cog_ext.cog_slash(name="uptime", description="Core - Shows the Bot's Uptime.")
    async def slashuptime(self, ctx: interactions.SlashContext):
        await self.uptime(ctx)
    
    @commands.command(name="bab", hidden=True)
    async def bab(self, ctx: commands.Context):
        """???"""

        await ctx.send("**Flamey** (developer of **BuildABot**) always puts a prefix-based Easter Egg in his bots. But this time... he didn't know what to do, because he can't predict prefixes!\nSo he did this. Nice find.")

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))