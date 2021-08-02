import discord
import json
import asyncpg
import discord_slash as interactions
from discord_slash import cog_ext
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'hidden': True})
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
        
    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command).rstrip(" ")

    def command_formatter(self, embed, command):
        embed.title = f"{self.get_command_signature(command)} (from {command.cog_name})"
        if command.description:
            embed.description = f'{command.description}\n\n{command.help}'
        else:
            embed.description = command.help or 'No help found'

    async def send_bot_help(self, mapping):
        ctx = self.context

        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.context.bot.user.id}\n%'")
        bot = q.splitlines()

        embed = discord.Embed(title=f"{bot[5]}'s Commands", color=int(bot[7], 16), description=f"This is a list of Commands for {bot[5]}.")
        embed.set_author(name=self.embed["author"].replace("name", bot[5]) + "Help", icon_url=bot[6])
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        botx = self.context.bot
        filtered = await self.filter_commands(botx.commands, sort=True)
        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands)
            if filtered:
                embed.add_field(name=f"{cog.qualified_name}", value=cog.description or 'No description', inline=False)
                for command in filtered:
                    embed.add_field(name=f"`{self.get_command_signature(command)}`", value=f"{command.description}\n\n{command.short_doc}", inline=False)
        embed.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.context.bot.user.id}\n%'")
        bot = q.splitlines()

        embed = discord.Embed(title=f"{self.get_command_signature(command)} (from {command.cog_name})", description=command.help or 'No description', color=int(bot[7], 16))
        embed.set_author(name=self.embed["author"].replace("name", bot[5]) + "Help", icon_url=bot[6])
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        embed.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.context.bot.user.id}\n%'")
        bot = q.splitlines()

        embed = discord.Embed(color=int(bot[7], 16))
        embed.set_author(name=self.embed["author"].replace("name", bot[5]) + "Help", icon_url=bot[6])
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        embed.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        self.command_formatter(embed, group)

        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.context.bot.user.id}\n%'")
        bot = q.splitlines()

        embed = discord.Embed(title=f"{cog.qualified_name}", description=cog.description or 'No description', color=int(bot[7], 16))
        embed.set_author(name=self.embed["author"].replace("name", bot[5]) + "Help", icon_url=bot[6])
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                self.add_command_field(embed, command)
        embed.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await self.context.send(embed=embed)

class Help(commands.Cog):
    """The Bot's `help` Command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self
        with open("./postgres.json") as postgresfile:
            self.postgres = json.load(postgresfile)
        with open("./BuildABot/BuildABot/misc/bots/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    async def pgselect(self, query: str):
        db: asyncpg.Connection = await asyncpg.connect(self.postgres["buildabot"])
        return await db.fetchrow(f'''{query}''')

    def cog_unload(self):
        self.bot.help_command = self.old_help_command
    
    @cog_ext.cog_slash(name="help", description="Help - Get help about all Commands.")
    async def slashhelp(self, ctx: interactions.SlashContext):
        q: str = await self.pgselect(f"SELECT bots FROM bab WHERE bots = '%\n{self.bot.user.id}\n%'")
        bot = q.splitlines()

        corec = ""
        func = ""
        helpc = ""
        utilityc = ""

        for key, value in self.bot.slash.commands:
            description = value["description"].split(" - ")

            if description[0] == "Core":
                corec += f"`{key}` - `{description[1]}\n\n"
            elif description[0] == "Fun":
                func += f"`{key}` - `{description[1]}\n\n"
            elif description[0] == "Help":
                helpc += f"`{key}` - `{description[1]}\n\n"
            elif description[0] == "Utility":
                utilityc += f"`{key}` - `{description[1]}\n\n"
        
        corec = corec.rstrip()
        func = func.rstrip()
        helpc = helpc.rstrip()
        utilityc = utilityc.rstrip()

        cogs = bot[4].split(":")

        e = discord.Embed(title=f"{bot[5]}'s Slash Commands", color=int(bot[7], 16), description=f"The following is a list of Slash Commands for {bot[5]}.")
        e.set_author(name=self.embed["author"].replace("name", bot[5]) + "Help", icon_url=bot[6])
        e.add_field(name="Core", value=corec, inline=False)
        e.add_field(name="Help", value=helpc, inline=False)
        if "fun" in cogs:
            e.add_field(name="Fun", value=func, inline=False)
        if "utility" in cogs:
            e.add_field(name="Utility", value=utilityc, inline=False)
        e.set_footer(text=self.embed["footer"].replace("name", bot[5]), icon_url=bot[6])
        await ctx.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))