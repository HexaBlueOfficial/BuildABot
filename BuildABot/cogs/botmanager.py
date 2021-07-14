import discord
import json
import asyncpg
import aiohttp
import discord_slash as interactions
from discord_slash import cog_ext
from discord.ext import commands

class BothChangesNoneType(Exception):
    def __init__(self):
        super().__init__("Both name and avatar arguments are NoneType.")

class BotManager(commands.Cog):
    """Bot managing Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./token.json") as tokenfile:
            self.token = json.load(tokenfile)
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    async def pgexecute(self, sql: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        await db.execute(f'''{sql}''')

    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    @commands.command(name="create")
    async def create(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/create`."""

        await ctx.send("Please use the Slash Command version, over at `/create`.")
    
    @cog_ext.cog_slash(name="create", description="Create a Bot!", options=[
        interactions.utils.manage_commands.create_option("name", "The bot's name.", 3, True),
        interactions.utils.manage_commands.create_option("avatar", "The bot's avatar.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/wwio.jpg", "Hammer and Wrench"),
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/605t.jpg", "Sky")
        ])
    ])
    @commands.has_permissions(manage_guild=True)
    async def _create(self, ctx: interactions.SlashContext, name: str, avatar: str):
        await ctx.defer()

        q = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '{ctx.guild.id}\n%'")
        if q is None:
            async with aiohttp.ClientSession(headers={"Authorization": self.token["bab"]["builder"]}) as session:
                async with session.post("https://discord.com/api/v9/applications", data={"name": name}) as application:
                    response1 = await application.json()
                    appid = response1["id"]
                    async with session.post(f"https://discord.com/api/v9/applications/{appid}/bot", data={"username": name, "avatar": avatar}) as bot:
                        response2 = await bot.json()
                        token = response2["token"]
                        await self.pgexecute(f"INSERT INTO bab(bots) VALUES ('{ctx.guild.id}\n{appid}\n{token}\nx')")
        
            e = discord.Embed(title="Bot Created Successfully", color=int(self.embed["color"], 16), description="Click the link below to add your Bot!")
            e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
            e.add_field(name="Invite", value=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={appid}&permissions=8&scope=bot%20applications.commands) to invite your Bot!")
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

            components = [
                interactions.utils.manage_components.create_actionrow(
                    interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blurple, "Get Bot Info", None, "botinfo1")
                )
            ]
            create = await ctx.send(embed=e, components=components)

            waitfor = await interactions.utils.manage_components.wait_for_component(self.bot, create, "botinfo1")

            user = await self.bot.fetch_user(appid)
            
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
    async def edit(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/edit`."""

        await ctx.send("Please use the Slash Command version, over at `/edit`.")
    
    @cog_ext.cog_slash(name="edit", description="Change your Bot's name or avatar!", options=[
        interactions.utils.manage_commands.create_option("name", "The Bot's new name.", 3, False),
        interactions.utils.manage_commands.create_option("avatar", "The Bot's new avatar.", 3, False, choices=[
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/wwio.jpg", "Hammer and Wrench"),
            interactions.utils.manage_commands.create_choice("https://this.is-for.me/i/605t.jpg", "Sky")
        ])
    ])
    @commands.has_permissions(manage_guild=True)
    async def _edit(self, ctx: interactions.SlashContext, name: str=None, avatar: str=None):
        await ctx.defer()

        if name is None and avatar is None:
            raise BothChangesNoneType
        
        if name is None:
            name = ""
        if avatar is None:
            avatar = ""

        q = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '{ctx.guild.id}\n%'")
        if q is not None:
            async with aiohttp.ClientSession(headers={"Authorization": f"Bot {q.splitlines()[2]}"}) as session:
                async with session.patch("https://discord.com/api/v9/users/@me", data={"username": name, "avatar": avatar}) as response:
                    response = await response.json()

                    e = discord.Embed(title="Bot Edited Successfully", color=int(self.embed["color"], 16), description="Your changes were successfully applied.")
                    e.set_author(name=self.embed["author"] + "Bot Manager", icon_url=self.embed["icon"])
                    e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        
                    components = [
                        interactions.utils.manage_components.create_actionrow(
                            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blurple, "Get Bot Info", None, "botinfo2")
                        )
                    ]
                    create = await ctx.send(embed=e, components=components)

                    waitfor = await interactions.utils.manage_components.wait_for_component(self.bot, create, "botinfo2")

                    user = await self.bot.fetch_user(response["id"])
            
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
    
    @commands.command(name="delete")
    @commands.has_permissions(manage_guild=True)
    async def delete(self, ctx: commands.Context):
        """Delete your Bot."""

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
    
    @cog_ext.cog_slash(name="delete", description="Delete your Bot.")
    @commands.has_permissions(manage_guild=True)
    async def _delete(self, ctx: interactions.SlashContext):
        await ctx.defer()
        
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

def setup(bot: commands.Bot):
    bot.add_cog(BotManager(bot))