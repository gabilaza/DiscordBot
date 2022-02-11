
import asyncio
import discord
import youtube_dl
from discord.ext import commands


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Playlist:
    def __init__(self):
        self.queue = []
        self.loop = "None"
        self.indexQ = 0


    def repeat(self, option):
        if option == '':
            if self.loop == "None":
                self.loop = "Repeat1"
            elif self.loop == "Repeat1":
                self.loop = "RepeatQueue"
            elif self.loop == "RepeatQueue":
                self.loop = "None"
            return f'```Repeat: {self.loop}```'
        else:
            if option == 'None' or option == '->':
                self.loop = 'None'
                return f'```Repeat: {self.loop}```'
            elif option == 'Repeat1' or option == '1':
                self.loop = 'Repeat1'
                return f'```Repeat: {self.loop}```'
            elif option == 'RepeatQueue' or option == 'l':
                self.loop = 'RepeatQueue'
                return f'```Repeat: {self.loop}```'
            else:
                return '```The option is not correct```'


    def add(self, url):
        self.queue.append(url)


    def show(self):
        if self.queue:
            return f'```Queue:\n - '+'\n - '.join(self.queue)+'```'
        else:
            return '```Queue is empty```'


    def clear(self):
        self.queue = []
        self.indexQ = 0
        return '```Queue cleared```'


    def next_song(self):
        if self.loop == "None":
            del(self.queue[self.indexQ])
            if self.indexQ != 0:
                self.indexQ = 0
        elif self.loop == "Repeat1":
            pass
        elif self.loop == "RepeatQueue":
            self.indexQ += 1
            if self.indexQ >= len(self.queue):
                self.indexQ = 0


    def get_song(self):
        if self.queue:
            return self.queue[self.indexQ]
        return None



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop = "None"
        self.indexQ = 0
        self.playlists = {}


    def get_playlist(self, ctx):
        try:
            playlist = self.playlists[ctx.guild.id]
        except:
            playlist = Playlist()
            self.playlists[ctx.guild.id] = playlist

        return playlist


    @commands.command()
    @commands.guild_only()
    async def repeat(self, ctx, option=''):
        """Repeat songs (None or ->, Repeat1 or 1, RepeatQueue or l)"""
        playlist = self.get_playlist(ctx)
        s = playlist.repeat(option)
        await ctx.send(s)


    @commands.command()
    @commands.guild_only()
    async def qadd(self, ctx, *, url):
        """Add song"""
        playlist = self.get_playlist(ctx)
        playlist.add(url)


    @commands.command()
    @commands.guild_only()
    async def qshow(self, ctx):
        """Show songs"""
        playlist = self.get_playlist(ctx)
        s = playlist.show()
        await ctx.send(s)


    @commands.command()
    @commands.guild_only()
    async def qclear(self, ctx):
        """Clear songs"""
        playlist = self.get_playlist(ctx)
        s = playlist.clear()
        await ctx.send(s)


    @commands.command()
    @commands.guild_only()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    async def play_next(self, ctx):
        playlist = self.get_playlist(ctx)
        playlist.next_song()
        if playlist.get_song():
            await self.play(ctx)


    @commands.command()
    @commands.guild_only()
    async def play(self, ctx):
        """Play the queue"""
        playlist = self.get_playlist(ctx)
        if playlist.get_song():
            def handleNext(error, ctx):
                if error:
                    print('Player error: %s' % error)
                else:
                    asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

            player = await YTDLSource.from_url(playlist.get_song(), loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: handleNext(e, ctx))
            await ctx.send(f'```Now playing: {player.title}```')
        else:
            await ctx.send("```Queue is empty```")


    @commands.command()
    @commands.guild_only()
    async def skip(self, ctx):
        """Play next song"""
        ctx.voice_client.stop()


    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        """Disconnects the bot from voice"""
        del(self.playlists[ctx.guild.id])
        await ctx.voice_client.disconnect()


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("```You are not connected to a voice channel.```")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

