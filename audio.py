import discord
from discord.ext import commands
from datetime import datetime

import youtube_dl
import asyncio
import os

class cat_audio(commands.Cog, name="Audio commands"):
    """Documentation"""

    def __init__(self, bot):
        self.bot = bot
        self.playlist = []
        
    class YTDLSource(discord.PCMVolumeTransformer):

        youtube_dl.utils.bug_reports_message = lambda: ""
        music_folder = "/tmp/discord-bot/"
        
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get("title")
            self.url = ""
            os.system(f"mkdir -p {self.music_folder}")

        @classmethod
        def ytdl():
            ytdl_format_options = {
            "format": "bestaudio/best",
            "restrictfilenames": True,
            "noplaylist": True,
            "outtmpl": self.music_folder + "%(title)s.%(ext)s",
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
            }
            ffmpeg_options = {"options": "-vn"}
            ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
            return ytdl

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):

            print(f"YTDLSource.from_url")
            loop = loop or asyncio.get_event_loop()
            print("ytdl_url_0")
            data = await loop.run_in_executor(
                None, lambda: ytdl().extract_info(url, download=not stream)
            )
            print("ytdl_url_1")
            if "entries" in data:
                # take first item from a playlist
                data = data["entries"][0]
            print("ytdl_url_2")
            filename = data["title"] if stream else ytdl().prepare_filename(data)
            print("ytdl_url_3")
            return filename


    async def add_to_playlist(self, ctx, url):
        '''function to be called to add url or keywords to play musics in thing'''
        print(f"add_to_playlist")
        if type(url) == list:
            url = " ".join(url)
        if type(url) != str:
            ctx.send(f"Fudeu: ErrIntern, url not str, it's {type(url)}")
            return
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
            return
        print(url)
        self.playlist.append(url)
        if len(self.playlist) == 1:
            await self.true_play(ctx, self.playlist[0])


    async def true_play(self, ctx, url):
        '''the one that really plays the music'''
        print(f"true_play")
        # connecting to the channel
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
            voice_channel = ctx.voice_client
            async with ctx.typing():
                filename = await self.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                print(filename)
                voice_channel.play(
                    discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                    #after=next(ctx),
                )
            await ctx.send(f"**Now playing:** {filename}")
        except Exception as e:
            await ctx.send(f"Fudeu: {e}")


    @commands.command(name="play", help="To play song")
    async def play(self, ctx, url):
        print(f"[{datetime.now()}] Command Issued: play\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        await add_to_playlist(ctx, url)


    @commands.command(name="pause", help="This command pauses the song")
    async def pause(self, ctx):
        print(f"[{datetime.now()}] Command Issued: pause\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")


    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        print(f"[{datetime.now()}] Command Issued: resume\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")


    @commands.command(name='next', help='plays next song')
    async def next(self, ctx):
        print(f"[{datetime.now()}] Command Issued: next\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        '''does a auto next'''
        playlist.pop(0)
        if len(playlist) != 0:
            await true_play(ctx, playlist[0])


    @commands.command(name="queue", help="Lists songs")
    async def queue(self, ctx):
        print(f"[{datetime.now()}] Command Issued: queue\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        if len(playlist) == 0:
            await ctx.send("No videos :(, add with `!play song`")
        else:
            printable_queue = "Requests on list:\n```\n"
            for item in playlist:
                printable_queue = "{}{}\n".format(printable_queue, item)
            await ctx.send("{}\n```".format(printable_queue))


    @commands.command(name="leave", help="To make the bot leave the voice channel")
    async def leave(self, ctx):
        print(f"[{datetime.now()}] Command Issued: leave\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        voice_client = ctx.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command(name="stop", help="Stops the song")
    async def stop(self, ctx):
        print(f"[{datetime.now()}] Command Issued: stop\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")


    @commands.command()
    async def yamete(self, ctx):
        await self.add_to_playlist(ctx, "https://www.youtube.com/watch?v=50bnHZLMqTI")

    @commands.command()
    async def sus(self, ctx):
        await self.add_to_playlist(ctx, "https://www.youtube.com/watch?v=grd-K33tOSM")

    @commands.command()
    async def jojo(self, ctx):
        await self.add_to_playlist(ctx, "https://www.youtube.com/watch?v=2MtOpB5LlUA")

    @commands.command()
    async def thunder(self, ctx):
        await self.add_to_playlist(ctx, "https://www.youtube.com/watch?v=bB-d7bc63CE")

def setup(bot):
    bot.add_cog(cat_audio(bot))