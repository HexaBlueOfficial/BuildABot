import discord
import json
import asyncpg
import typing
import discord_slash as interactions
from ..misc.bab.extracode import bans
from discord_slash import cog_ext
from discord.ext import commands

class Utility(commands.Cog):
    """Utility Commands!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    async def userinfo(self, ctx: typing.Union[commands.Context, interactions.SlashContext], user: str=None):
        if bans.check(ctx):
            await bans.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        if user is None:
            string = ""
            for role in ctx.author.roles:
                if role == ctx.guild.default_role:
                    continue
                string = string + f"{role.mention} "

            e = discord.Embed(title=f"Information for {str(ctx.author)}", color=int(bot[7], 16))
            e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Utility", icon_url=bot[6])
            e.set_thumbnail(url=ctx.author.avatar_url)
            e.add_field(name="Username", value=f"{ctx.author.name}")
            e.add_field(name="Discriminator", value=f"{ctx.author.discriminator}")
            e.add_field(name="ID", value=f"{ctx.author.id}")
            if ctx.author.nick is not None:
                e.add_field(name="Nickname", value=f"{ctx.author.nick}")
            e.add_field(name="Status", value=f"{ctx.author.status}")
            if ctx.author.activity is not None:
                e.add_field(name="Activity", value=f"{ctx.author.activity}")
            e.add_field(name="Color", value=f"{ctx.author.color}")
            e.add_field(name="Joined At", value="{} UTC".format(ctx.author.joined_at.strftime("%A, %d %B %Y at %H:%M")))
            e.add_field(name="Created At", value="{} UTC".format(ctx.author.created_at.strftime("%A, %d %B %Y at %H:%M")))
            e.add_field(name="Roles", value=string)
            e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
            await ctx.send(embed=e)
        else:
            try:
                user = int(user)
            except:
                user = str(user).lstrip("<@!")
                user = user.rstrip(">")
                user = int(user)

                user = self.bot.get_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                string = ""
                for role in user.roles:
                    if role == ctx.guild.default_role:
                        continue
                    string = string + f"{role.mention} "

                e = discord.Embed(title=f"Information for {str(user)}", color=int(bot[7], 16))
                e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Utility", icon_url=bot[6])
                e.set_thumbnail(url=user.avatar_url)
                e.add_field(name="Username", value=f"{user.name}")
                e.add_field(name="Discriminator", value=f"{user.discriminator}")
                e.add_field(name="ID", value=f"{user.id}")
                if user.nick is not None:
                    e.add_field(name="Nickname", value=f"{user.nick}")
                e.add_field(name="Status", value=f"{user.status}")
                if user.activity is not None:
                    e.add_field(name="Activity", value=f"{user.activity}")
                e.add_field(name="Color", value=f"{user.color}")
                e.add_field(name="Joined At", value="{} UTC".format(user.joined_at.strftime("%A, %d %B %Y at %H:%M")))
                e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                e.add_field(name="Roles", value=string)
                e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
                await ctx.send(embed=e)
            else:
                user = await self.bot.fetch_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                    string = ""
                    for role in user.roles:
                        if role == ctx.guild.default_role:
                            continue
                        string = string + f"{role.mention} "

                    e = discord.Embed(title=f"Information for {str(user)}", color=int(bot[7], 16))
                    e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Utility", icon_url=bot[6])
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    if user.nick is not None:
                        e.add_field(name="Nickname", value=f"{user.nick}")
                    e.add_field(name="Status", value=f"{user.status}")
                    if user.activity is not None:
                        e.add_field(name="Activity", value=f"{user.activity}")
                    e.add_field(name="Color", value=f"{user.color}")
                    e.add_field(name="Joined At", value="{} UTC".format(user.joined_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.add_field(name="Roles", value=string)
                    e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
                    await ctx.send(embed=e)
                else:
                    e = discord.Embed(title=f"Information for {str(user)}", color=int(bot[7], 16))
                    e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Utility", icon_url=bot[6])
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
                    await ctx.send(embed=e)
    
    @commands.command(name="userinfo", aliases=["ui"])
    async def dpyinfouser(self, ctx: commands.Context, user: str=None):
        """Gets info about a User."""

        await ctx.trigger_typing()
        await self.userinfo(ctx, user)
    
    @cog_ext.cog_subcommand(base="info", name="user", description="Utility - Gets info about a User.", options=[
        interactions.utils.manage_commands.create_option("user", "The User to get information about.", 3, False)
    ])
    async def slashinfouser(self, ctx: interactions.SlashContext, user: str=None):
        await self.userinfo(ctx, user)
    
    async def serverinfo(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bans.check(ctx):
            await bans.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        memberCount = 0
        botCount = 0
        for member in ctx.guild.members:
            if member.bot:
                botCount = botCount + 1
            else:
                memberCount = memberCount + 1
            
        string = ""
        for role in ctx.guild.roles:
            if role == ctx.guild.default_role:
                continue
            if role.name == "‎‎‎‎":
                continue
            string = string + f"{role.mention} "
            
        e = discord.Embed(title=f"Information for {ctx.guild.name}", color=int(bot[7], 16))
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Utility", icon_url=bot[6])
        e.set_thumbnail(url=ctx.guild.icon.url)
        e.add_field(name="Name", value=f"{ctx.guild.name}")
        e.add_field(name="Owner", value=f"{str(ctx.guild.owner)}")
        e.add_field(name="ID", value=f"{ctx.guild.id}")
        e.add_field(name="User Count", value=f"{len(ctx.guild.members)}")
        e.add_field(name="Member Count", value=f"{memberCount}")
        e.add_field(name="Bot Count", value=f"{botCount}")
        e.add_field(name="Emojis", value=f"{len(ctx.guild.emojis)}")
        e.add_field(name="Created At", value="{} UTC".format(ctx.guild.created_at.strftime("%A, %d %B %Y at %H:%M")))
        e.add_field(name="Roles", value=string)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="serverinfo", aliases=["si", "guildinfo", "gi"])
    async def dpyinfoserver(self, ctx: commands.Context):
        """Gets info about the Server you're in."""

        await ctx.trigger_typing()
        await self.serverinfo(ctx)
    
    @cog_ext.cog_subcommand(base="info", name="server", description="Gets info about the Server you're in.")
    async def slashinfoserver(self, ctx: interactions.SlashContext):
        await self.serverinfo(ctx)
    
def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))