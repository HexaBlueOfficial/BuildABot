import discord
import json
import asyncpg
import typing
import aiohttp
import discord_slash as interactions
import random
import asyncio
from ..misc.bab.extracode import bancheck
from ..misc.bab.extracode import supermarket
from discord_slash import cog_ext
from discord.ext import commands

class Fun(commands.Cog):
    """Fun Commands!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
        with open("./BuildABot/BuildABot/misc/bots/lines/8ball.json") as eightballfile:
            self.eightballl = json.load(eightballfile)
        with open("./BuildABot/BuildABot/misc/bots/lines/gay.json") as gayfile:
            self.gay = json.load(gayfile)
        with open("./BuildABot/BuildABot/misc/bots/lines/hug.json") as hugfile:
            self.hugg = json.load(hugfile)
        with open("./BuildABot/BuildABot/misc/bots/lines/kill.json") as killfile:
            self.killl = json.load(killfile)
        with open("./BuildABot/BuildABot/misc/bots/lines/supermarket.json") as marketfile:
            self.supermarkett = json.load(marketfile)
    
    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')
    
    def uwufy(self, sentence: str):
        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
        uwu = uwu.replace("ove", "uv")
        return f"{uwu}, uwu *rawr* XD!"
    
    async def cat(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search/") as response:
                cat = await response.json()
                catpic = cat[0]["url"]
        
        e = discord.Embed(title="Random Cat (from TheCatAPI by Aden)", color=int(bot[7], 16), description="Check out TheCatAPI [here](https://thecatapi.com)!")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_image(url=catpic)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)

    @commands.command(name="cat")
    async def dpycat(self, ctx: commands.Context):
        """Shows a random image of a cat."""

        await ctx.trigger_typing()
        await self.cat(ctx)
    
    @cog_ext.cog_subcommand(base="animals", name="cat", description="Fun - Shows a random image of a cat.")
    async def slashcat(self, ctx: interactions.SlashContext):
        await self.cat(ctx)
    
    async def dog(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search/") as response:
                dog = await response.json()
                dogpic = dog[0]["url"]
        
        e = discord.Embed(title="Random Dog (from TheDogAPI by Aden)", color=int(bot[7], 16), description="Check out TheDogAPI [here](https://thedogapi.com)!")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_image(url=dogpic)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="dog")
    async def dpydog(self, ctx: commands.Context):
        """Shows a random image of a dog."""

        await ctx.trigger_typing()
        await self.dog(ctx)
    
    @cog_ext.cog_subcommand(base="animals", name="dog", description="Fun - Shows a random image of a dog.")
    async def slashdog(self, ctx: interactions.SlashContext):
        await self.dog(ctx)
    
    async def fox(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as response:
                fox = await response.json()
                foxpic = fox["image"]
        
        e = discord.Embed(title="Random Fox (from Random Fox by xinitrc)", color=int(bot[7], 16), description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_image(url=foxpic)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="fox")
    async def dpyfox(self, ctx: commands.Context):
        """Shows a random image of a fox."""

        await ctx.trigger_typing()
        await self.fox(ctx)
    
    @cog_ext.cog_subcommand(base="animals", name="fox", description="Fun - Shows a random image of a fox.")
    async def slashfox(self, ctx: interactions.SlashContext):
        await self.fox(ctx)
    
    @commands.command(name="say")
    async def dpysay(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/say`."""

        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        await ctx.send("Please use the Slash Command version, over at `/say`.")
    
    @cog_ext.cog_slash(name="say", description="Fun - The Bot will say what you tell it to.", options=[
        interactions.utils.manage_commands.create_option("message", "What you want the Bot to say.", 3, True),
        interactions.utils.manage_commands.create_option("anonymous", "Whether you want the message author to be anonymous or not.", 5, False),
        interactions.utils.manage_commands.create_option("uwu", "Wud you wike youw message to wook wike a fuwwy wwote it?", 5, False),
        interactions.utils.manage_commands.create_option("user", "The User you want to \"impersonate\".", 6, False)
    ])
    async def slashsay(self, ctx: interactions.SlashContext, message: str, anonymous: bool=False, uwu: bool=False, user: discord.Member=None):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        if anonymous:
            avatar = await self.bot.user.avatar.read()
            webhook = await ctx.channel.create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
        elif user is None:
            avatar = await ctx.author.avatar.read()
            webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")
        else:
            avatar = await user.avatar.read()
            webhook = await ctx.channel.create_webhook(name=user.name, avatar=avatar, reason="Say command.")
        
        if uwu:
            await webhook.send(self.uwufy(message))
        else:
            await webhook.send(message)
        
        slashbug = await ctx.send("e")
        await slashbug.delete()

        await webhook.delete()

    async def eightball(self, ctx: typing.Union[commands.Context, interactions.SlashContext], question: str):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        balllineint = random.randint(0, 4)
        ballline = self.eightballl[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=int(bot[7], 16))
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="8ball")
    async def dpy8ball(self, ctx: commands.Context, *, question: str):
        """Seek an answer from the Magic 8 Ball."""

        await self.eightball(ctx, question)
    
    @cog_ext.cog_slash(name="8ball", description="Fun - Seek an answer from the Magic 8 Ball.", options=[
        interactions.utils.manage_commands.create_option("question", "Your question for the Magic 8 Ball.", 3, True)
    ])
    async def slash8ball(self, ctx: interactions.SlashContext, question: str):
        await self.eightball(ctx, question)
    
    async def gaypercent(self, ctx: typing.Union[commands.Context, interactions.SlashContext], thing: str=None):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        gay = random.randint(0, 100)
        supergay = random.randint(1, 10)

        def makeline(jsonline):
            halfpoint = self.gay[jsonline].replace("thing", thing)
            gayliner = halfpoint.replace("gaypercent", f"{gay}%")
            return gayliner
        
        def line():
            if gay == 0:
                gayline = makeline("0")
            elif gay <= 25:
                gayline = makeline("1to25")
            elif gay <= 50:
                gayline = makeline("26to50")
            elif gay <= 75:
                gayline = makeline("51to75")
            elif gay <= 99:
                gayline = makeline("76to99")
            elif gay == 100:
                gayline = makeline("100")
            elif gay > 100:
                gayline = makeline("over100")
            return gayline

        if thing is None:
            thing = ctx.author.mention

            if supergay == 8:
                gay = gay * 10
            
            gayline = line()
        else:
            try:
                gayid = int(thing)
            except:
                if supergay == 8:
                    gay = gay * 10
            
                gayline = line()
            else:
                thing = self.bot.fetch_user(gayid)

                if supergay == 8:
                    gay = gay * 10
            
                gayline = line()
            
        e = discord.Embed(title="Gay Percentage", color=int(bot[7], 16), description=f"{gayline}")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="gaypercent")
    async def dpygay(self, ctx: commands.Context, *, thing: str=None):
        """Wanna find out how gay something is? This command is for you."""

        await self.gaypercent(ctx, thing)
    
    @cog_ext.cog_slash(name="gaypercent", description="Fun - Wanna find out how gay something is? This command is for you.", options=[
        interactions.utils.manage_commands.create_option("thing", "What you want to find the gayness of.", 3, False)
    ])
    async def slashgay(self, ctx: interactions.SlashContext, thing: str=None):
        await self.gaypercent(ctx, thing)
    
    async def hug(self, ctx: typing.Union[commands.Context, interactions.SlashContext], member: discord.Member, message: str=None):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        huglineint = random.randint(0, 9)
        halfpoint = self.hugg[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=int(bot[7], 16), description=f"{hugline}")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! They said...", value=f"{message}", inline=False)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="hug")
    async def dpyhug(self, ctx: commands.Context, member: discord.Member, message: str=None):
        """Hugs the Member you want."""

        await self.hug(ctx, member, message)
        await ctx.message.delete()
    
    @cog_ext.cog_slash(name="hug", description="Fun - Hugs the Member you want.", options=[
        interactions.utils.manage_commands.create_option("member", "The Member to hug.", 6, True),
        interactions.utils.manage_commands.create_option("message", "A message to add.", 3, False)
    ])
    async def slashhug(self, ctx: interactions.SlashContext, member: discord.Member, message: str=None):
        await self.hug(ctx, member, message)
    
    async def kill(self, ctx: typing.Union[commands.Context, interactions.SlashContext], member: discord.Member):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        killlineint = random.randint(0, 4)
        halfpoint = self.killl[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=int(bot[7], 16), description=f"{killline}")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)
    
    @commands.command(name="kill")
    async def dpykill(self, ctx: commands.Context, member: discord.Member):
        """Kills the Member you want."""

        await self.kill(ctx, member)
    
    @cog_ext.cog_slash(name="kill", description="Fun - Kills the Member you want.", options=[
        interactions.utils.manage_commands.create_option("member", "The Member to kill.", 6, True)
    ])
    async def slashkill(self, ctx: interactions.SlashContext, member: discord.Member):
        await self.kill(ctx, member)
    
    async def supermarket(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        supermarketint = random.randint(0, 2)
        supermarkett = self.supermarkett["products"][str(supermarketint)]

        buttons = []
        for product in supermarkett:
            product = product.splitlines()
            buttons.append(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blurple, product[1], None, product[2])
            )
        components = [interactions.utils.manage_components.create_actionrow(*buttons)]

        hintint = 0 # random.randint(0, 4)
        hint = self.supermarkett["hints"][str(hintint)]

        e = discord.Embed(title="Welcome to the Supermarket!", color=int(bot[7], 16), description="Pick a code!\nWill you be lucky enough?")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        supermarketmsg = await ctx.send(f"Hint: {hint}", embed=e, components=components)

        ids = ["M.dev*command+cert", "R.hug", "R.kill", "DB.user@updates", "M.user+amogass", "M.user+ff", "M.user+whensus", "M.user+amogus", "M.dev*roast+cert", "DB.bot*1mo@plus"]
        waitfor: interactions.ComponentContext = await interactions.utils.manage_components.wait_for_component(self.bot, supermarketmsg, ids)
        if waitfor.author.id == ctx.author.id:
            if waitfor.custom_id.startswith("M."):
                await supermarket.message(ctx, self.bot, waitfor.custom_id.lstrip("M."))
            elif waitfor.custom_id.startswith("R."):
                await supermarket.run(ctx, bot, waitfor.custom_id.lstrip("R."))
            elif waitfor.custom_id.startswith("DB."):
                await supermarket.database(ctx, bot, waitfor.custom_id.lstrip("DB."))
    
    @commands.command(name="supermarket")
    async def dpysupermarket(self, ctx: commands.Context):
        """Welcome to the Supermarket! Pick a product!"""

        await self.supermarket(ctx)
    
    @cog_ext.cog_slash(name="supermarket", description="Fun - Welcome to the Supermarket! Pick a product!")
    async def slashsupermarket(self, ctx: interactions.SlashContext):
        await self.supermarket(ctx)
    
    @commands.command(name="poll")
    async def dpypoll(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/poll`."""

        await ctx.send("Please use the Slash Command version, over at `/poll`.")
    
    @cog_ext.cog_slash(name="poll", description="Fun - Create a poll. Currently only supports two options.", options=[
        interactions.utils.manage_commands.create_option("name", "The poll's name.", 3, True),
        interactions.utils.manage_commands.create_option("option1", "The first option to vote on.", 3, True),
        interactions.utils.manage_commands.create_option("option2", "The second option to vote on.", 3, True)
    ])
    async def slashpoll(self, ctx: interactions.SlashContext, name: str, option1: str, option2: str):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        vote1 = 0
        vote2 = 0
        
        e = discord.Embed(title=f"Poll: {name}", color=int(bot[7], 16), description=f"**Poll by {ctx.author.mention}.**\nThink and choose.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.add_field(name=option1, value=f"{vote1} | 0%")
        e.add_field(name=option2, value=f"{vote2} | 0%")
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        poll = await ctx.send(embed=e, components=[
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "1st Option", None, "opt1"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "2nd Option", None, "opt2")
            )
        ])

        while 0 == 0:
            waitfor: interactions.ComponentContext = await interactions.utils.manage_components.wait_for_component(self.bot, poll, ["opt1", "opt2"])
            e.clear_fields()
            if waitfor.custom_id == "opt1":
                vote1 += 1
            elif waitfor.custom_id == "opt2":
                vote2 += 1
            operation1 = round((vote1 * 100) / (vote1 + vote2), 1)
            operation2 = round((vote2 * 100) / (vote1 + vote2), 1)
            if str(operation1).endswith(".0"):
                operation1 = round(operation1)
            if str(operation2).endswith(".0"):
                operation2 = round(operation2)
            e.add_field(name=option1, value=f"{vote1} | {operation1}")
            e.add_field(name=option2, value=f"{vote2} | {operation2}")
            await waitfor.edit_origin(embed=e)
    
    @commands.command(name="calculator")
    async def dpycalculator(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/calculator`."""

        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        await ctx.send("Please use the Slash Command version, over at `/calculator`.")
    
    @cog_ext.cog_slash(name="calculator", description="Fun - Calculate.")
    async def slashcalculator(self, ctx: interactions.SlashContext):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        string = ""

        actionrow1 = interactions.utils.manage_components.create_actionrow(
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "7", None, "7"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "8", None, "8"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "9", None, "9"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "+", None, "+"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.red, "Close", None, "exit")
        )
        actionrow2 = interactions.utils.manage_components.create_actionrow(
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "4", None, "4"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "5", None, "5"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "6", None, "6"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "-", None, "-"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.red, "←", None, "back")
        )
        actionrow3 = interactions.utils.manage_components.create_actionrow(
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "1", None, "1"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "2", None, "2"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "3", None, "3"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "*", None, "*"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.red, "Clear", None, "clear")
        )
        actionrow4 = interactions.utils.manage_components.create_actionrow(
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "00", None, "00"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, "0", None, "0"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.grey, ".", None, "."),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "/", None, "/"),
            interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.green, "=", None, "=")
        )

        components = [actionrow1, actionrow2, actionrow3, actionrow4]

        e = discord.Embed(title=f"{ctx.author.name}'s Calculator", color=int(self.embed["color"], 16), description="```\n \n```")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=self.embed["icon"])
        calculatormessage = await ctx.send(embed=e, components=components)

        async def check1(string):
            try:
                if string.split("|")[-2] == "+":
                    return False
                elif string.split("|")[-2] == "-":
                    return False
                elif string.split("|")[-2] == "*":
                    return False
                elif string.split("|")[-2] == "/":
                    return False
            except:
                return True
            else:
                return False
        
        async def check2(string):
            try:
                if string.split("|")[-2] == "+":
                    return False
                elif string.split("|")[-2] == "-":
                    return False
                elif string.split("|")[-2] == "*":
                    return False
                elif string.split("|")[-2] == "/":
                    return False
                elif "+" in string.split("|"):
                    return False
                elif "-" in string.split("|"):
                    return False
                elif "*" in string.split("|"):
                    return False
                elif "/" in string.split("|"):
                    return False
            except:
                return True
            else:
                return False
        
        while 0 == 0:
            waitfor: interactions.ComponentContext = await interactions.utils.manage_components.wait_for_component(self.bot, calculatormessage, ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "=", "exit", "back", "clear"])
            if waitfor.author.id == ctx.author.id:
                try:
                    int(waitfor.custom_id)
                except:
                    if waitfor.custom_id == "exit":
                        e.description = "```\nThis Calculator has been closed.\n```"

                        symbols = ["+", "-", "*", "/"]
                        stuff = ["exit", "back", "clear"]
                        for actionrow in components:
                            for i in range(5):
                                style = None
                                try:
                                    int(actionrow[i].custom_id)
                                except:
                                    if actionrow[i].custom_id in symbols:
                                        style = interactions.utils.manage_components.ButtonStyle.blurple
                                    elif actionrow[i].custom_id in stuff:
                                        style = interactions.utils.manage_components.ButtonStyle.red
                                    elif actionrow[i].custom_id == "=":
                                        style = interactions.utils.manage_components.ButtonStyle.green
                                    elif actionrow[i].custom_id == ".":
                                        style = interactions.utils.manage_components.ButtonStyle.grey
                                else:
                                    style = interactions.utils.manage_components.ButtonStyle.grey
                                actionrow[i] = interactions.utils.manage_components.create_button(style, actionrow[i].label, None, actionrow[i].custom_id, None, True)
                        await waitfor.edit_origin(embed=e, components=components)

                        await waitfor.send("Calculator closed.", hidden=True)
                        break
                    elif waitfor.custom_id == "back":
                        stringx = list(string).pop()
                        string = ""
                        for character in stringx:
                            string += character
                        stringe = string.replace("|", "")
                        e.description = f"```\n{stringe}\n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "clear":
                        string = ""
                        e.description = f"```\n \n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "=":
                        stringx = string.split("|")
                        operation = 0
                        if stringx[1] == "+":
                            operation = float(stringx[0]) + float(stringx[2])
                        elif stringx[1] == "-":
                            operation = float(stringx[0]) - float(stringx[2])
                        elif stringx[1] == "*":
                            operation = float(stringx[0]) * float(stringx[2])
                        elif stringx[1] == "/":
                            operation = float(stringx[0]) / float(stringx[2])
                        if str(operation).endswith(".0"):
                            operation = int(operation)
                        string = f"{operation}"
                        e.description = f"```\n{string}\n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "+":
                        if await check2(string):
                            string += "|+|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "-":
                        if await check2(string):
                            string += "|-|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "*":
                        if await check2(string):
                            string += "|*|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "/":
                        if await check2(string):
                            string += "|/|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == ".":
                        if check1(string):
                            string += waitfor.custom_id
                            e.description = f"```\n{string}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                else:
                    string += waitfor.custom_id
                    stringe = string.replace("|", "")
                    e.description = f"```\n{stringe}\n```"
                    await waitfor.edit_origin(embed=e)
    
    async def hack(self, ctx: typing.Union[commands.Context, interactions.SlashContext], user: discord.Member):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        hacking = await ctx.send("<a:aLoading:833070225334206504> **Getting logins...**")
        await asyncio.sleep(1.0)
        await hacking.edit(content="<:Yes:833293078197829642> **Logins deciphered. Select what to hack below.**")
        
        e = discord.Embed(title=f"Hack {user.name}", color=int(bot[7], 16), description=f"**Hacking {user.name} ready.**")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        hackmessage = await hacking.reply(embed=e, components=[
            interactions.utils.manage_components.create_actionrow(
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.blue, "Hack Discord", None, custom_id="discord"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.red, "Hack YouTube", None, custom_id="youtube"),
                interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.green, "Hack Twitter", None, custom_id="twitter")
            )
        ])

        waitfor: interactions.ComponentContext = await interactions.utils.manage_components.wait_for_component(self.bot, hackmessage, ["discord", "youtube", "twitter"])
        if waitfor.author_id == ctx.author.id:
            avatar = await user.avatar_url.read()
            webhook = await ctx.channel.create_webhook(name=user.name, avatar=avatar, reason="Hack command")
            if waitfor.custom_id == "discord":
                await webhook.send("I got hacked, oh fuck.")
                await webhook.send(f"FUCK! {ctx.author} HACKED ME!")
                e.description = "**DISCORD HACKED!**"
            elif waitfor.custom_id == "youtube":
                await webhook.send("I just posted a video!\nhttps://youtu.be/Blh2FCAIIgk")
                e.description = "**YOUTUBE HACKED!**"
            elif waitfor.custom_id == "twitter":
                await webhook.send("I just tweeted!\nhttps://twitter.com/theEarthNet/status/1402642068200165383")
                e.description = "**TWITTER HACKED!**"
            await waitfor.edit_origin(embed=e)
            await webhook.delete()
    
    @commands.context(name="hack")
    async def dpyhack(self, ctx: commands.Context, user: discord.Member):
        """Hack a Member (100% real)!"""

        await self.hack(ctx, user)
    
    @cog_ext.cog_slash(name="hack", description="Fun - Hack a Member (100% real)!", options=[
        interactions.utils.manage_commands.create_option("user", "Who to hack.", 6, True)
    ])
    async def slashhack(self, ctx: interactions.SlashContext, user: discord.Member):
        await self.hack(ctx, user)
    
    @commands.command(name="game")
    async def dpygame(self, ctx: commands.Context):
        """Please use the Slash Command version, over at `/discord game <subcommand>`."""

        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        await ctx.send("Please use the Slash Command version, over at `/discord game <subcommand>`.")
    
    @cog_ext.cog_subcommand(base="discord", subcommand_group="game", name="play", description="Fun - Play a Discord Game in a Voice Channel!", options=[
        interactions.utils.manage_commands.create_option("game", "The Discord Game to play.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("755827207812677713", "Poker Night"),
            interactions.utils.manage_commands.create_choice("832012774040141894", "Chess in the Park"),
            interactions.utils.manage_commands.create_choice("755600276941176913", "YouTube Together"),
            interactions.utils.manage_commands.create_choice("773336526917861400", "Betrayal.io"),
            interactions.utils.manage_commands.create_choice("814288819477020702", "Fishington.io")
        ])
    ])
    async def slashgameplay(self, ctx: interactions.SlashContext, game: str):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        async def playgame(channel: discord.VoiceChannel):
            invite = await channel.create_invite(target_type=discord.InviteTarget.embedded_application, target_application_id=int(game), reason="Play Discord Game Command.")

            gamex = ""
            if game == "755827207812677713":
                gamex = "Poker Night"
            elif game == "832012774040141894":
                gamex = "Chess in the Park"
            elif game == "755600276941176913":
                gamex = "YouTube Together"
            elif game == "773336526917861400":
                gamex = "Betrayal.io"
            elif game == "814288819477020702":
                gamex = "Fishington.io"
        
            e = discord.Embed(title=f"Play {gamex}!", color=int(bot[7], 16), description=f"Click the Button below to play {gamex} in the {channel.name} Voice Channel!")
            e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
            e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
            await ctx.send(embed=e, components=[
                interactions.utils.manage_components.create_actionrow(
                    interactions.utils.manage_components.create_button(interactions.utils.manage_components.ButtonStyle.URL, f"Play {gamex}!", None, None, invite.url)
                )
            ])
        
        voicestatus = ctx.author.voice

        if voicestatus is None:
            await ctx.send("Please join a Voice Channel and run the command again.", hidden=True)
        else:
            await playgame(voicestatus.channel)
    
    @cog_ext.cog_subcommand(base="discord", subcommand_group="game", name="info", description="Fun - Get info about Discord Games", options=[
        interactions.utils.manage_commands.create_option("game", "The Discord Game to get information about.", 3, True, choices=[
            interactions.utils.manage_commands.create_choice("Discord Games", "Discord Games (in general)"),
            interactions.utils.manage_commands.create_choice("Poker Night", "Poker Night"),
            interactions.utils.manage_commands.create_choice("Chess in the Park", "Chess in the Park"),
            interactions.utils.manage_commands.create_choice("YouTube Together", "YouTube Together"),
            interactions.utils.manage_commands.create_choice("Betrayal.io", "Betrayal.io"),
            interactions.utils.manage_commands.create_choice("Fishington.io", "Fishington.io")
        ])
    ])
    async def slashgameinfo(self, ctx: interactions.SlashContext, game: str):
        if bancheck.check(ctx):
            await bancheck.banned(ctx)
            return

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        if game != "Discord Games":
            gameid = 0
            if game == "Poker Night":
                gameid = 755827207812677713
            elif game == "Chess in the Park":
                gameid = 832012774040141894
            elif game == "YouTube Together":
                gameid = 755600276941176913
            elif game == "Betrayal.io":
                gameid = 773336526917861400
            elif game == "Fishington.io":
                gameid = 814288819477020702
        
        gamedesc = ""
        if game == "Discord Games":
            gamedesc = "**Discord Games** are a **Beta** Discord feature, released **randomly** in some servers. There are six in total."
        elif game == "Poker Night":
            gamedesc = "Play poker with your friends in your favourite Discord server thanks to **Poker Night**. This was the first game released.\n**According to Discord themselves, *Poker Night* should only be played by people older than 18.**"
        elif game == "Chess in the Park":
            gamedesc = "Play a nice game of chess in a chill park with **Chess in the Park**. This game is the latest released."
        elif game == "YouTube Together":
            gamedesc = "Watch YouTube videos with all your friends thanks to **YouTube Together**!"
        elif game == "Betrayal.io" or game == "Fishington.io":
            gamedesc = "**Description coming soon(er or later).**"

        e = discord.Embed(title=f"About {game}", color=int(bot[7], 16))
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Fun", icon_url=bot[6])
        if game != "Discord Games":
            e.add_field(name="Name", value=f"{game}")
            e.add_field(name="ID", value=f"{gameid}")
        e.add_field(name="Description", value=f"{gamedesc}")
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))