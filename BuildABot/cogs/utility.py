import discord
import json
import typing
import discord_slash as interactions
from datetime import datetime
from discord_slash import cog_ext
from discord.ext import commands

class Utility(commands.Cog):
    """Utility Commands for BuildABot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()

    async def ping(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        ping = round(self.bot.latency * 1000, 1)

        e = discord.Embed(title="Ping Latency", color=int(self.embed["color"], 16), description=f"My Ping Latency is {ping}ms.")
        e.set_author(name=self.embed["author"] + "Utility", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="ping", aliases=["latency", "lat"])
    async def dpyping(self, ctx: commands.Context):
        """Gets BuildABot's Ping Latency."""

        await self.ping(ctx)
    
    @cog_ext.cog_slash(name="ping", description="Gets BuildABot's Ping Latency.")
    async def slashping(self, ctx: interactions.SlashContext):
        await self.ping(ctx)
    
    async def uptime(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=int(self.embed["color"], 16), description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name=self.embed["author"] + "Utility", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Last Restart", value="The Bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="uptime")
    async def dpyuptime(self, ctx: commands.Context):
        """Shows BuildABot's Uptime."""

        await self.uptime(ctx)
    
    @cog_ext.cog_slash(name="uptime", description="Shows BuildABot's Uptime.")
    async def slashuptime(self, ctx: interactions.SlashContext):
        await self.uptime(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))