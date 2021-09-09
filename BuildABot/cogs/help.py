import discord
import json
import dinteractions_Paginator as paginator
from ..misc.bab.extracode import bans
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'hidden': True})
        with open("./BuildABot/BuildABot/misc/bab/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self.context, command).rstrip(" ")

    def command_formatter(self, embed, command):
        embed.title = f"{self.get_command_signature(command)} (from {command.cog_name})"
        if command.description:
            embed.description = f'{command.description}\n\n{command.help}'
        else:
            embed.description = command.help or 'No help found'

    async def send_bot_help(self, mapping):
        ctx = self.context

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        embed = discord.Embed(title="BuildABot's Commands", color=int(self.embed["color"], 16), description="The following is a list of Commands for BuildABot.")
        embed.set_author(name=self.embed["author"] + "Help", icon_url=self.embed["icon"])
        embed.set_thumbnail(url=self.embed["icon"])
        bot = ctx.bot
        filtered = await self.filter_commands(bot.commands, sort=True)
        embeds = [embed]
        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands)
            if filtered:
                e = discord.Embed(title=f"{cog.qualified_name}", color=int(self.embed["color"], 16), description=cog.description or 'No description')
                e.set_author(name=self.embed["author"] + "Help", icon_url=self.embed["icon"])
                for command in filtered:
                    e.add_field(name=f"`{self.get_command_signature(command)}`", value=f"{command.description}\n\n{command.short_doc}", inline=False)
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                embeds.append(e)
        embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await paginator.Paginator(bot, ctx, embeds)

    async def send_command_help(self, command):
        ctx = self.context

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        embed = discord.Embed(title=f"{self.get_command_signature(command)} (from {command.cog_name})", description=command.help or 'No description', color=int(self.embed["color"], 16))
        embed.set_author(name=self.embed["author"] + "Help", icon_url=self.embed["icon"])
        embed.set_thumbnail(url=self.embed["icon"])
        embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        embed = discord.Embed(color=int(self.embed["color"], 16))
        embed.set_author(name=self.embed["author"] + "Help", icon_url=self.embed["icon"])
        embed.set_thumbnail(url=self.embed["icon"])
        embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        self.command_formatter(embed, group)

        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context

        if bans.check(ctx):
            await bans.banned(ctx)
            return

        embed = discord.Embed(title=f"{cog.qualified_name}", description=cog.description or 'No description', color=int(self.embed["color"], 16))
        embed.set_author(name=self.embed["author"] + "Help", icon_url=self.embed["icon"])
        embed.set_thumbnail(url=self.embed["icon"])
        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                self.add_command_field(embed, command)
        embed.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await ctx.send(embed=embed)

class Help(commands.Cog):
    """BuildABot's `help` Command!"""
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

def setup(bot):
    bot.add_cog(Help(bot))