import discord
from discord.ext import commands
from datetime import datetime

class cat_debug(commands.Cog, name="Debug commands"):
    """Documentation"""

    def __init__(self, bot):
        self.bot = bot

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        filename = data["title"] if stream else ytdl.prepare_filename(data)
        return filename

playlist = []

music_folder = "/tmp/discord-bot/"
os.system(f"mkdir -p {music_folder}")

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "outtmpl": music_folder + "%(title)s.%(ext)s",
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

@bot.command(name='next', help='plays next song')
async def next(ctx: Context):
    '''does a auto next'''
    playlist.pop(0)
    if len(playlist) != 0:
        await true_play(ctx, playlist[0])


async def add_to_playlist(ctx: Context, url):
    '''function to be called to add url or keywords to play musics in thing'''
    if type(url) == list:
        url = " ".join(url)
    if type(url) != str:
        ctx.send(f"Fudeu: ErrIntern, url not str, it's {type(url)}")
        return
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    print(url)
    playlist.append(url)
    if len(playlist) == 1:
        await true_play(ctx, playlist[0])


async def true_play(ctx: Context, url):
    '''the one that really plays the music'''
    # connecting to the channel
    print(f"true_play")
    channel = ctx.message.author.voice.channel
    try:
        await channel.connect()
        voice_channel = ctx.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            print(filename)
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                #after=next(ctx),
            )
        await ctx.send(f"**Now playing:** {filename}")
    except Exception as e:
        await ctx.send(f"Fudeu: {e}")



@bot.command(name="play", help="To play song")
async def play(ctx: Context, url):
    await add_to_playlist(ctx, url)


@bot.command(name="pause", help="This command pauses the song")
async def pause(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name="resume", help="Resumes the song")
async def resume(ctx: Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send(
            "The bot was not playing anything before this. Use play_song command"
        )


@bot.command(name="queue", help="Lists songs")
async def queue(ctx: Context):
    if len(playlist) == 0:
        await ctx.send("No videos :(, add with `!play song`")
    else:
        printable_queue = "Requests on list:\n```\n"
        for item in playlist:
            printable_queue = "{}{}\n".format(printable_queue, item)
        await ctx.send("{}\n```".format(printable_queue))



@bot.command(name="leave", help="To make the bot leave the voice channel")
async def leave(ctx: Context):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name="stop", help="Stops the song")
async def stop(ctx: Context):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command()
async def yamete(ctx: Context):
    await add_to_playlist(ctx, "https://www.youtube.com/watch?v=50bnHZLMqTI")

@bot.command()
async def sus(ctx: Context):
    await add_to_playlist(ctx, "https://www.youtube.com/watch?v=grd-K33tOSM")

@bot.command()
async def jojo(ctx: Context):
    await add_to_playlist(ctx, "https://www.youtube.com/watch?v=2MtOpB5LlUA")

@bot.command()
async def thunder(ctx: Context):
    await add_to_playlist(ctx, "https://www.youtube.com/watch?v=bB-d7bc63CE")