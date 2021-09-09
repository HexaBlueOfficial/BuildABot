import typing
import discord
import json
import asyncpg
import discord_slash as interactions
from ..misc.bab.extracode import bans
from ..misc.bab.extracode import paid
from discord_slash import cog_ext
from discord.ext import commands

class Developer(commands.Cog):
    """Developer-only Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./token.json") as tokenfile:
            self.token = json.load(tokenfile)
        with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    async def pgexecute(self, sql: str, stuff: str=None):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        if stuff is None:
            await db.execute(f'''{sql}''')
        else:
            await db.execute(f'''{sql}''', stuff)

    async def pgselect(self, query: str):
        db: asyncpg.Connection = asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    async def guilds(self, ctx: typing.Union[commands.Context, interactions.SlashContext], get: str):
        data = f""
        for guild in self.bot.guilds:
            if get == "name":
                data += f"{guild.name}\n"
            elif get == "id":
                data += f"{guild.id}\n"
            elif get == "owner":
                data += f"{str(guild.owner)}\n"
            elif get == "invite":
                invite = await guild.text_channels[0].create_invite(reason="Developer \"Guilds\" Command", max_uses=3)
                data += f"{invite.url}\n"
            elif get == "all":
                invite = await guild.text_channels[0].create_invite(reason="Developer \"Guilds\" Command", max_uses=3)
                data += f"{guild.name} | {guild.id} | {str(guild.owner)} | {invite.url}\n"
        data = data.rstrip()
        
        e = discord.Embed(title=f"Guilds [get=\"{get}\"]", color=int(self.embed["color"], 16), description=data)
        e.set_author(name=self.embed["author"] + "Developer", icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="guilds")
    @commands.is_owner()
    async def dpyguilds(self, ctx: commands.Context, get: str):
        """Gets all the Guilds the Bot is in.\nThis is a Developer-only Command."""

        await self.guilds(ctx, get)
    
    @cog_ext.cog_slash(name="guilds", description="Developer - Gets all the Guilds the Bot is in.", options=[
        interactions.utils.manage_commands.create_option("get", "What to get.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("all", "Everything"),
            interactions.utils.manage_commands.create_choice("name", "Guild Names"),
            interactions.utils.manage_commands.create_choice("id", "Guild IDs"),
            interactions.utils.manage_commands.create_choice("owner", "Guild Owners"),
            interactions.utils.manage_commands.create_choice("invite", "Guild Invites")
        ])
    ], default_permission=False, permissions={
        832594030264975420: [
            interactions.utils.manage_commands.create_permission(450678229192278036, 2, True)
        ],
        838718002412912661: [
            interactions.utils.manage_commands.create_permission(450678229192278036, 2, True)
        ]
    })
    async def slashguilds(self, ctx: interactions.SlashContext, get: str):
        await self.guilds(ctx, get)
    
    @cog_ext.cog_subcommand(base="db", subcommand_group="table", name="create", description="Developer - Creates a table in the database.", options=[
        interactions.utils.manage_commands.create_option("name", "Table name.", 3, True),
        interactions.utils.manage_commands.create_option("otherstuff", "Dev knows what's going on.", 3, True)
    ], default_permission=False, permissions={
        832594030264975420: [
            interactions.utils.manage_commands.create_permission(450678229192278036, 2, True)
        ],
        838718002412912661: [
            interactions.utils.manage_commands.create_permission(450678229192278036, 2, True)
        ]
    })
    async def dbtablecreate(self, ctx: interactions.SlashContext, name: str, otherstuff: str):
        await self.pgexecute(f"CREATE TABLE {name} ({otherstuff})")
        await ctx.send("Done.")

def setup(bot: commands.Bot):
    bot.add_cog(Developer(bot))