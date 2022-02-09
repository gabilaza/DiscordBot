
import asyncio
import subprocess
import json
import discord
from discord.ext import commands
from domain.music import Music
from domain.githubscore import GithubScore
from domain.challenge import Challenge


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botlogout(self, ctx):
        """Bot logout"""
        await ctx.invoke(self.bot.get_command('ghsave'))
        await ctx.invoke(self.bot.get_command('chsave'))
        await ctx.send('```Bye bye```')
        await self.bot.logout()


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description='I will help you', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('-----------------------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        await ctx.send('```I don\'t have this command :(```')
    raise error

bot.add_cog(Music(bot))
bot.add_cog(GithubScore(bot))
bot.add_cog(Bot(bot))
bot.add_cog(Challenge(bot))
TOKEN = 'my token'
bot.run(TOKEN)
