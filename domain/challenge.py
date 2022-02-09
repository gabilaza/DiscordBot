
import asyncio
import discord
import datetime
from discord.ext import commands


class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.challenges = {}
        self.scores = {}
        self.doneChallenges = {}

        with open('storageChallenge/members.txt', 'r') as f:
            for line in f.readlines():
                l = line.strip().split()
                self.scores[l[0]] = float(l[1])

        with open('storageChallenge/storage.txt', 'r') as f:
            for line in f.readlines():
                l = line.strip().split()
                s = ''
                for i in range(1, len(l)-1):
                    if i == 1:
                        s += l[i]
                    else:
                        s += ' '+l[i]
                self.challenges[l[0]] = [s, float(l[-1])]

        with open('storageChallenge/done.txt', 'r') as f:
            for line in f.readlines():
                l = line.strip().split()
                if l[0] in self.doneChallenges:
                    self.doneChallenges[l[0]].append(l[1])
                else:
                    self.doneChallenges[l[0]] = [l[1]]


    @commands.command()
    @commands.guild_only()
    async def chshow(self, ctx):
        """Show the challenge for today"""
        today = str(datetime.date.today())
        if today in self.challenges:
            await ctx.send(f'```{self.challenges[today][0]} | Points: {self.challenges[today][1]}```')
        else:
            await ctx.send('```We don\'t have a challenge for this day```')


    @commands.command()
    @commands.guild_only()
    async def chsshow(self, ctx):
        """Show the scores of the people that are in challenge do"""
        s = 'ChallengeScores:\n'
        members = {}
        for member in ctx.guild.members:
            name = member.name+'#'+member.discriminator
            if name in self.scores:
                members[name] = self.scores[name]
        members = sorted(members.items(), key=lambda x:x[1], reverse=True)
        for member in members:
            s += f' - {member[0]} : {member[1]}\n'
        if s != 'ChallengeScores:\n':
            await ctx.send(f'```{s}```')
        else:
            await ctx.send('```None of this server has registered for challenge do```')


    @commands.command()
    @commands.guild_only()
    async def chcomplete(self, ctx):
        """Complete the challege for this day"""
        authorName = ctx.author.name+'#'+ctx.author.discriminator
        today = str(datetime.date.today())
        if authorName in self.scores:
            if today not in self.doneChallenges:
                self.doneChallenges[today] = []
            if authorName not in self.doneChallenges[today]:
                await ctx.send('```Congratulation!!!```')
                self.scores[authorName] += self.challenges[today][1]
                self.doneChallenges[today].append(authorName)
            else:
                await ctx.send('```You did the challenge for today.```')
        else:
            await ctx.send('```You are not in the list```')


    @commands.command()
    @commands.guild_only()
    async def chregister(self, ctx):
        """Register for Challenge"""
        authorName = ctx.author.name+'#'+ctx.author.discriminator
        if authorName not in self.scores:
            self.scores[authorName] = 0
            await ctx.send('```Register complete```')
        else:
            await ctx.send('```You are in the list```')


    @commands.command()
    @commands.guild_only()
    async def chdeleteme(self, ctx):
        """Delete me from ChallengeScore"""
        authorName = ctx.author.name+'#'+ctx.author.discriminator
        if authorName in self.scores:
            for e in self.doneChallenges:
                for i, el in enumerate(self.doneChallenges[e]):
                    if el == authorName:
                        del(self.doneChallenges[e][i])
            del(self.scores[authorName])
            await ctx.send('```Delete complete```')
        else:
            await ctx.send('```You are not in the list```')


    @commands.command()
    @commands.guild_only()
    async def chsave(self, ctx):
        """Save ChallengeScore"""
        with open('storageChallenge/members.txt', 'w') as f:
            s = ''
            for member in self.scores:
                s += member+' '+str(self.scores[member])+'\n'
            f.write(s)

        with open('storageChallenge/done.txt', 'w') as f:
            s = ''
            for e in self.doneChallenges:
                for el in self.doneChallenges[e]:
                    s = s+e+' '+el+'\n'
            f.write(s)

        await ctx.send('```Save complete```')
