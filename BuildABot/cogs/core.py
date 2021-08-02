import discord
import json
import random
import typing
import platform
import discord_slash as interactions
from discord_slash import cog_ext
from discord.ext import commands, tasks

class Core(commands.Cog):
    """Core Commands for BuildABot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence.start()
        with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    @tasks.loop(seconds=400.0)
    async def presence(self):
        presences = {"playing": ["with Bots", "with API Requests"], "watching": ["you make your own Bot", "Bot makers"]}
        playorwatch = random.randint(1, 2)
        if playorwatch == 1:
            presencetouse = random.randint(0, 1)
            await self.bot.change_presence(activity=discord.Game(name=presences["playing"][presencetouse]))
        else:
            presencetouse = random.randint(0, 1)
            await self.bot.change_presence(activity=discord.Activity(name=presences["watching"][presencetouse], type=discord.ActivityType.watching))
    
    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener()
    async def on_ready(self):
        q: list = await self.pgselect(f"SELECT bots FROM bab")
        for bot in q:
            bot = bot.splitlines()

            botobj = commands.Bot(command_prefix=commands.when_mentioned_or(bot[3]), intents=discord.Intents.all())
            botobj.remove_command("help")

            extensions = ["..features.core", "..features.fun", "..features.help", "..features.utility"]
            for extension in extensions:
                botobj.load_extension(extension)
            
            await botobj.login(bot[2])
    
    async def info(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        luckyint = random.randint(1, 20)

        e = discord.Embed(title="About BuildABot", color=int(self.embed["color"], 16), description="**BuildABot** is a Bot... that makes Bots for who can't code!")
        e.set_author(name=self.embed["author"] + "Core", icon_url=self.embed["icon"])
        e.set_thumbnail(url=self.embed["icon"])
        e.add_field(name="Developers", value="<@450678229192278036>: All commands and their Slash equivalents.\n<@598325949808771083>: `bab help`.\nOther: `bab jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"BuildABot: v0.0.6\nPython: v{platform.python_version()}\ndiscord.py: v{discord.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)", inline=False)
        e.set_image(url=self.embed["banner"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        components = [
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "Invite", None, "invite"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, "Support", None, None, "https://discord.gg/bacZt25ZGZ")
            )
        ]
        info = await ctx.send(embed=e, components=components)

        if luckyint == 8:
            await ctx.author.send("Hey!")
            await ctx.author.send("You should try running `bab bab`!")

        waitfor: interactions.ComponentContext = await interactions.utils.manage_components.wait_for_component(self.bot, info, "invite")
        await waitfor.send("**Coming soon...**", hidden=True)

    @commands.command(name="info")
    async def info(self, ctx: commands.Context):
        """Shows information about BuildABot."""

        await self.info(ctx)
    
    @cog_ext.cog_slash(name="info", description="Core - Shows information about BuildABot.")
    async def _info(self, ctx: interactions.SlashContext):
        await self.info(ctx)
    
    @commands.command(name="bab", hidden=True)
    async def bab(self, ctx: commands.Context):
        await ctx.send("bab bab bab bab bab bab bab bab bab bab bab bab")

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))