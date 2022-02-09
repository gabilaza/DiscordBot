
import json
import asyncio
import discord
import subprocess
from discord.ext import commands


class GithubScore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores = {}
        self.ghUsername = {}

        with open('storageUser/members.txt', 'r') as f:
            for line in f.readlines():
                l = line.strip().split()
                self.scores[l[0]] = float(l[1])

        with open('storageUser/ghUser.txt', 'r') as f:
            for line in f.readlines():
                l = line.strip().split()
                self.ghUsername[l[0]] = l[1]


    def getCommitsCount(self, username):
        command = f'curl -H \'Accept: application/vnd.github.cloak-preview\' \https://api.github.com/search/commits?q=author:{username}'
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        output = json.loads(output)['total_count']
        if p_status:
            print(err)

        return output*0.2


    @commands.command()
    @commands.guild_only()
    async def ghshow(self, ctx):
        """Show the score of the people of the server on Github"""
        s = 'GithubScore:\n'
        members = {}
        for member in ctx.guild.members:
            name = member.name+'#'+member.discriminator
            if name in self.scores:
                members[name] = self.getCommitsCount(self.ghUsername[name])-self.scores[name]
        members = sorted(members.items(), key=lambda x:x[1], reverse=True)
        for member in members:
            s += f' - {member[0]} : {member[1]}\n'
        if s != 'GithubScore:\n':
            await ctx.send(f'```{s}```')
        else:
            await ctx.send('```None of this server has registered for GithubScore```')


    @commands.command()
    @commands.guild_only()
    async def ghregister(self, ctx, username):
        """Register for GithubScore"""
        authorName = ctx.author.name+'#'+ctx.author.discriminator
        if authorName not in self.scores:
            try:
                self.scores[authorName] = self.getCommitsCount(username)
                self.ghUsername[authorName] = username
                await ctx.send('```Register complete```')
            except:
                await ctx.send('```This username is not on Github```')
        else:
            await ctx.send('```You are in the list```')


    @commands.command()
    @commands.guild_only()
    async def ghdeleteme(self, ctx):
        """Delete me from GithubScore"""
        authorName = ctx.author.name+'#'+ctx.author.discriminator
        if authorName in self.scores:
            del(self.scores[authorName])
            del(self.ghUsername[authorName])
            await ctx.send('```Delete complete```')
        else:
            await ctx.send('```You are not in the list```')


    @commands.command()
    @commands.guild_only()
    async def ghsave(self, ctx):
        """Save GithubScore"""
        with open('storageUser/members.txt', 'w') as f:
            s = ''
            for member in self.scores:
                s += member+' '+str(self.scores[member])+'\n'
            f.write(s)

        with open('storageUser/ghUser.txt', 'w') as f:
            s = ''
            for member in self.ghUsername:
                s += member+' '+str(self.ghUsername[member])+'\n'
            f.write(s)

        await ctx.send('```Save complete```')

