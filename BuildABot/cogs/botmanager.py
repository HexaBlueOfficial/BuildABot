import discord
import json
import asyncpg
import discord_slash as interactions
import aiohttp
import typing
from ..misc.bab.extracode import bans
from discord_slash import cog_ext
from discord.ext import commands

class AllChangesNoneType(Exception):
    def __init__(self):
        super().__init__("You edited nothing.")

class BotManager(commands.Cog):
    """Bot-managing Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./token.json") as tokenfile:
            self.token = json.load(tokenfile)
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    async def pgexecute(self, sql: str, stuff: str=None):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        if stuff is None:
            await db.execute(f'''{sql}''')
        else:
            await db.execute(f'''{sql}''', stuff)

    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')

    @commands.command(name="create")
    async def dpycreate(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/create`."""

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        await ctx.send("Please use the Slash Command version, over at `/create`.")

    @cog_ext.cog_slash(name="create", description="Bot Manager - Create a Bot!", options=[
        interactions.utils.manage_commands.create_option("name", "The Bot's name.", 3, True),
        interactions.utils.manage_commands.create_option("prefix", "The Bot's prefix (symbol to which the bot will respond to).", 3, True),
        interactions.utils.manage_commands.create_option("features", "The plugins/Cogs for the Bot.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("core:help", "Core | Help"),
            interactions.utils.manage_commands.create_choice("core:help:fun", "Core | Help | Fun"),
            interactions.utils.manage_commands.create_choice("core:help:utility", "Core | Help | Utility"),
            interactions.utils.manage_commands.create_choice("core:help:fun:utility", "Core | Help | Fun | Utility")
        ]),
        interactions.utils.manage_commands.create_option("avatar", "The Bot's avatar.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/n2o6.jpg", "Hammer and Wrench"),
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/605t.jpg", "Sky")
        ])
    ])
    @commands.has_permissions(administrator=True)
    async def slashcreate(self, ctx: interactions.SlashContext, name: str, prefix: str, features: str, avatar: str):
        await ctx.defer()

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        q = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '{ctx.guild.id}\n%'")
        if q is None:
            botobj = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=discord.Intents.all())
            botobj.remove_command("help")

            async with aiohttp.ClientSession(headers={"Authorization": self.token["bab"]["builder"]}) as session1:
                async with session1.post("https://discord.com/api/v9/applications", json={"name": name, "team_id": "868533132880658483"}) as application:
                    response1 = await application.json()
                    appid = response1["id"]
                    await session1.patch(f"https://discord.com/api/v9/applications/{appid}", json={"description": f"{name} is a **Bot** created with **BuildABot**!\nCheck **BuildABot** out at https://buildabot.tk/"})
                async with session1.post(f"https://discord.com/api/v9/applications/{appid}/bot") as bot:
                    response2 = await bot.json()
                    token = response2["token"]

                    if avatar == "https://this.is-for.me/i/n2o6.jpg":
                        await self.pgexecute("INSERT INTO bab(bots) VALUES ($1)", f"{ctx.guild.id}\n{appid}\n{token}\n{prefix}\n{features}\n{name}\n{avatar}\nffffff")
                    elif avatar == "https://this.is-for.me/i/605t.jpg":
                        await self.pgexecute("INSERT INTO bab(bots) VALUES ($1)", f"{ctx.guild.id}\n{appid}\n{token}\n{prefix}\n{features}\n{name}\n{avatar}\n00a8ff")

            async with aiohttp.ClientSession(headers={"Authorization": f"Bot {token}"}) as session2:
                await session2.patch("https://discord.com/api/v9/users/@me", json={"avatar": avatar})

            botobj = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=discord.Intents.all())
            slashobj = interactions.SlashCommand(botobj, sync_commands=True, sync_on_cog_reload=True)
            botobj.remove_command("help")

            cogs = features.split(":")
            for cog in cogs:
                botobj.load_extension(f"..features.{cog}")

            await botobj.login(token)

            e = discord.Embed(title="Bot Created Successfully", color=int(self.embed["color"], 16), description="Click the link below to add your Bot!")
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.add_field(name="Invite", value=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={appid}&permissions=8&scope=bot%20applications.commands) to invite your Bot!")
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

            create = await ctx.send(embed=e, components=[
                interactions.utils.manage_components.create_actionrow(
                    interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blurple, "Get Bot Info", None, "botinfo1")
                )
            ])

            waitfor = await interactions.utils.manage_components.wait_for_component(self.bot, create, "botinfo1")

            user = await self.bot.fetch_user(int(appid))

            e = discord.Embed(title=f"Information about {str(user)}", color=int(self.embed["color"], 16))
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.set_thumbnail(url=user.avatar.url)
            e.add_field(name="Username", value=f"{user.name}", inline=False)
            e.add_field(name="Discriminator", value=f"{user.discriminator}", inline=False)
            e.add_field(name="ID", value=f"{user.id}", inline=False)
            e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")), inline=False)
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await waitfor.send(embed=e)
        else:
            guildbot = self.bot.get_user(q.splitlines()[1])

            e = discord.Embed(title=f"What about {guildbot.name}?", color=int(self.embed["color"], 16), description=f"It looks like you already have a Bot ({str(guildbot)}).\nIf you tried to run this Command again, it probably means you don't want it anymore, so please use the `/delete` or `bab delete` Command to remove it, and be able to make a new one.")
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ctx.send(embed=e)
    
    @commands.command(name="edit")
    async def dpyedit(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/edit`."""

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        await ctx.send("Please use the Slash Command version, over at `/edit`.")

    @cog_ext.cog_slash(name="edit", description="Bot Manager - Change your Bot's name or avatar!", options=[
        interactions.utils.manage_commands.create_option("name", "The Bot's new name.", 3, False),
        interactions.utils.manage_commands.create_option("features", "The plugins/Cogs for the Bot.", 3, False, choices=[
            interactions.utils.manage_commands.create_choice("core:help", "Core | Help"),
            interactions.utils.manage_commands.create_choice("core:help:fun", "Core | Help | Fun"),
            interactions.utils.manage_commands.create_choice("core:help:utility", "Core | Help | Utility"),
            interactions.utils.manage_commands.create_choice("core:help:fun:utility", "Core | Help | Fun | Utility")
        ]),
        interactions.utils.manage_commands.create_option("avatar", "The Bot's new avatar.", 3, False, choices=[
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/n2o6.jpg", "Hammer and Wrench"),
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/605t.jpg", "Sky")
        ])
    ])
    @commands.has_permissions(manage_guild=True)
    async def slashedit(self, ctx: interactions.SlashContext, name: str=None, features: str=None, avatar: str=None):
        await ctx.defer()

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        if name is None and features is None and avatar is None:
            raise AllChangesNoneType

        q = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '{ctx.guild.id}\n%'")
        if q is not None:
            bot: typing.List[str] = q.splitlines()

            if name is None:
                name = [bot[5], False]
            else:
                name = [name, True]
            if avatar is None:
                avatar = [bot[6], False]
            else:
                avatar = [avatar, True]

            if name[1] or avatar[1]:
                async with aiohttp.ClientSession(headers={"Authorization": f"Bot {bot[2]}"}) as session:
                    async with session.patch("https://discord.com/api/v9/users/@me", json={"username": name, "avatar": avatar}) as response:
                        response = await response.json()
            
            if features is not None:
                await self.pgexecute(f"UPDATE bab SET bots = $1 WHERE bots = '{ctx.guild.id}\n%'", f"{bot[0]}\n{bot[1]}\n{bot[2]}\n{bot[3]}\n{features}\n{bot[5]}\n{bot[6]}\n{bot[7]}")

            e = discord.Embed(title="Bot Edited Successfully", color=int(self.embed["color"], 16), description="Your changes were successfully applied.\n**If the Features were updated, please run `reload` (whether normal or Slash) on your Bot to get the newly added Commands!**")
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        
            components = [
                interactions.utils.manage_components.create_actionrow(
                    interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blurple, "Get Bot Info", None, "botinfo2")
                    )
                ]
            edit = await ctx.send(embed=e, components=components)

            waitfor = await interactions.utils.manage_components.wait_for_component(self.bot, edit, "botinfo2")

            user = await self.bot.fetch_user(int(response["id"]))
            
            e = discord.Embed(title=f"Information about {str(user)}", color=int(self.embed["color"], 16))
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.set_thumbnail(url=user.avatar.url)
            e.add_field(name="Username", value=f"{user.name}", inline=False)
            e.add_field(name="Discriminator", value=f"{user.discriminator}", inline=False)
            e.add_field(name="ID", value=f"{user.id}", inline=False)
            e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")), inline=False)
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await waitfor.send(embed=e)
        else:
            e = discord.Embed(title="Editing thin air!", color=int(self.embed["color"], 16), description="If you don't have a Bot in the first place... what do you want to edit? Your next Minecraft speedrun for your -1 subscriber YouTube channel?")
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ctx.send(embed=e)
    
    async def delete(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bans.check(ctx):
            await bans.banned(ctx)
            return

        q = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '{ctx.guild.id}\n%'")
        if q is not None:
            async with aiohttp.ClientSession(headers={"Authorization": self.token["bab"]["builder"]}) as session:
                async with session.post(f"https://discord.com/api/v9/applications/{q.splitlines()[1]}/delete"):
                    await self.pgexecute(f"DELETE FROM bab WHERE bots = '{ctx.guild.id}\n%'")
            
            e = discord.Embed(title="Bot Deleted Successfully", color=int(self.embed["color"], 16), description="We're sorry to see you go!")
        else:
            e = discord.Embed(title="Wait...", color=int(self.embed["color"], 16), description="You don't even have a Bot!")

        e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="delete")
    @commands.has_permissions(manage_guild=True)
    async def dpydelete(self, ctx: commands.Context):
        """Delete your Bot."""

        await ctx.trigger_typing()
        await self.delete(ctx)
    
    @cog_ext.cog_slash(name="delete", description="Bot Manager - Delete your Bot.")
    @commands.has_permissions(manage_guild=True)
    async def slashdelete(self, ctx: interactions.SlashContext):
        await ctx.defer()
        await self.delete(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(BotManager(bot))