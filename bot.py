import discord
import youtube_dl
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
import discord
import youtube_dl
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
import os
import random

import asyncio
import os
import random


intents = discord.Intents().default()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")

music_folder = "/tmp/discord-bot/"
os.system(f"mkdir -p {music_folder}")

##########################################################################
##########################################################################
################################ AUDIO ###################################
##########################################################################
##########################################################################


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
playlist_status=0
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
    await internal_next(ctx)

@bot.command(name="cona")
async def cona(ctx : Context):
    await ctx.send(
        f"Eu só quero {ctx.author.name} 😳"
    )
async def internal_next(ctx :Context):
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
        await ctx.send(
            f"{ctx.message.author.name} is not connected to a voice channel"
        )
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    playlist.append(url)
    if len(playlist) == 1:
        playlist_status = 0
        await true_play(ctx, playlist[0])



async def true_play(ctx: Context, url):
    '''the one that really plays the music'''
    # connecting to the channel
    channel = ctx.message.author.voice.channel
    try:
        await channel.connect()
    except:
        pass
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                after=await internal_next(ctx)
            )
        await ctx.send(f"**Now playing:** {filename}")
    except:
        await ctx.send("The bot is not connected to a voice channel.")
    except Exception as e:
        err = f"Fudeu: {e}"
        print(err)
        await ctx.send(err)


@bot.command(name="play", help="To play song")
async def play(ctx: Context, *, url):
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
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name="stop", help="Stops the song")
async def stop(ctx: Context):
    voice_client = ctx.message.guild.voice_client
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




##########################################################################
##########################################################################
######################### TEXT BOT STUFF #################################
##########################################################################
##########################################################################


@bot.command(name="cona")
async def cona(ctx):
    await ctx.send(f"Eu só quero {ctx.author.name} 😳")


@bot.event
async def on_ready():
    print("Running!")
    for guild in bot.guilds:
        # for channel in guild.text_channels:
            # if str(channel) == "general":
                # await channel.send("Bot Activated..")
                # await channel.send(file=discord.File("giphy.png"))
        # if str(channel) == "general":
        # await channel.send("Bot Activated..")
        # await channel.send(file=discord.File("giphy.png"))
        print(f"Active in {guild.name}\n Member Count : {guild.member_count}")


@bot.command(help="Prints details of Author")
async def whats_my_name(ctx : Context):
    await ctx.send(f"Hello {ctx.author.name}")




@bot.command(help="Prints details of Server")
async def where_am_i(ctx: Context):
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description

    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members = []
    async for member in ctx.guild.fetch_members(limit=150):
        await ctx.send(
            f"Name : {member.display_name}\t Status : {str(member.status)}\n Joined at {str(member.joined_at)}")


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if str(channel) == "general":
            on_mobile = False
            if member.is_on_mobile() == True:
                on_mobile = True
            await channel.send(
                f"Welcome to the Server {member.name}!!\n On Mobile : {on_mobile}")

##########################################################################
############################# Battle #####################################
##########################################################################

@bot.command(name="battle", help="Battle with another user")
async def battle(ctx: Context):
    if ctx.author.id == ctx.message.mentions[0].id:
        await ctx.send("Don't battle yourself, you LONER!")
        return
    winner = ctx.author.id if random.randint(0, 1) == 0 else ctx.message.mentions[0].id
    await ctx.send(f"<@{winner}> has the biggest dick!!!")


@bot.command(name="battle", help="Battle with another user!")
async def battle(ctx : Context, mention : discord.Member):
    if ctx.author.name == mention.display_name:
        msg = "Don't battle yourself, you LONER!"
    else:
        i = random.randint(0,1000)
        if i%2 == 0:
            msg = f"{ctx.author.name} wins!!!"
        else:
            msg = f"{mention.display_name} wins!!!"
    #msg = "".ctx.author.name
    await ctx.send(msg)

@battle.error
async def battle_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I could not find that member... do `!battle @adversary`")
    else:
        await ctx.send(f"A batalha fudeu: {error}")


##########################################################################
############################# DOILOVE ####################################
##########################################################################


@bot.command(name="doilove", help="FInd out how compatible are you with another user")
async def doilove(ctx: Context):
    if len(ctx.message.mentions) == 0:
        await ctx.send("Yes you do! But WHO is the question... do `!doilove @person`")
    lovemeter = (69 - (ctx.author.id - ctx.message.mentions[0].id) % 69 + 5) % 11
    rest = 10 - lovemeter
    msg = "["
    while lovemeter > 0:
        msg += f"❤️"
        lovemeter -= 1
    while rest > 0:
        msg += f"🤍"
        rest -= 1
    msg += "]"
    await ctx.send(f"<3 Love meter Ɛ> {msg}")

@bot.command()
async def tell_me_about_yourself(ctx: Context):
    text = "My name is OnikenX's pet!\n I was built originally by Kakarot2000. I'm now ~~a slave to OnikenX~~ OnikenX's loyal pet, you can see my services with !help.\n :)"
    await ctx.send(text)

@bot.event
async def on_message(message):
    # bot.process_commands(msg) is a couroutine that must be called here since we are overriding the on_message event
    await bot.process_commands(message)
    if str(message.content).lower() == "hello":
        await message.channel.send("Hi!")

    if str(message.content).lower() in ["swear_word1", "swear_word2"]:
        await message.channel.purge(limit=1)


##########################################################################
##########################################################################
############################# DEBUGGING ##################################
##########################################################################
##########################################################################

@bot.command()
async def test_args(ctx : commands):
    await ctx.send(f"Mensagem: {ctx}")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
