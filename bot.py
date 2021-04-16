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


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

load_dotenv()
# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")


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
    playlist.append(url)
    if len(playlist) == 1:
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
                after=next(ctx),
            )
        print("fiz download e corri")
        await ctx.send(f"**Now playing:** {filename}")
    except Exception as e:
        await ctx.send(f"Fudeu: {e}")



@bot.command(name="play", help="To play song")
async def play(ctx: Context, url):
    print("lets generic")
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
####################### NORMAL BOT STUFF #################################
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
        print(f"Active in {guild.name}\n Member Count : {guild.member_count}")


@bot.command(help="Prints details of Author")
async def whats_my_name(ctx: Context):
    await ctx.send(f"Hello {ctx.author.name}")




@bot.command(help="Prints details of Server")
async def where_am_i(ctx: Context):
    print("Command Issued: where_am_i\n   - message: {}\n   - debug: {}".format(ctx.message.content, ctx.message))
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

    #Requires Privileged Gateway Intents - Server Members Intent Enabled.
    #members = []
    #async for member in ctx.guild.fetch_members(limit=150):
    #    await ctx.send(
    #        "Name : {}\t Status : {}\n Joined at {}".format(
    #            member.display_name, str(member.status), str(member.joined_at)
    #        )
    #    )


@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if str(channel) == "general":
            on_mobile = False
            if member.is_on_mobile() == True:
                on_mobile = True
            await channel.send(
                "Welcome to the Server {}!!\n On Mobile : {}".format(
                    member.name, on_mobile
                )
            )

        # TODO : Filter out swear words from messages

################################################################
@bot.command(name="battle", help="Battle with another user")
async def battle(ctx: Context):
    print("Command Issued: battle\n   - message: {}\n   - debug: {}".format(ctx.message.content, ctx.message))
    if ctx.author.id == ctx.message.mentions[0].id:
        await ctx.send("Don't battle yourself, you LONER!")
        return
    winner = ctx.author.id if random.randint(0, 1) == 0 else ctx.message.mentions[0].id
    await ctx.send(f"<@{winner}> has the biggest dick!!!")


@battle.error
async def battle_error(ctx: Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I could not find that member... do `!battle @adversary`")
    else:
        await ctx.send(f"A batalha fudeu: {error}")

@bot.command(name="doilove", help="FInd out how compatible are you with another user")
async def doilove(ctx: Context):
    print("Command Issued: doilove\n   - message: {}\n   - debug: {}".format(ctx.message.content, ctx.message))
    if len(ctx.message.mentions) == 0:
        await ctx.send("Yes you do! But WHO is the question... do `!doilove @person`")
        return
    lovemeter = (69 - (ctx.message.author.id - ctx.message.mentions[0].id) % 69 + 4) % 11
    red = lovemeter
    white = 10 - lovemeter
    msg = "<3 Love meter Ɛ> ["
    while red > 0:
        msg += f"❤️"
        red -= 1
    while white > 0:
        msg += f"🖤"
        white -= 1
    msg += "]"
    lovemeter = int(lovemeter/2)
    if lovemeter == 0:
        msg += "\nA better romance than Crepusculo! 💔"
    if lovemeter == 1:
        msg += "\nYou don't need love, as long as there's a hole"
    if lovemeter == 2:
        msg += "\nMaybe with some effort... and dick picks"
    if lovemeter == 3:
        msg += "\nAs good as your hand!"
    if lovemeter == 4:
        msg += "\nDamn, {} must give you lots of wet dreams!!"
    if lovemeter == 5:
        msg += "\nDamn, {} must give you lots of wet dreams!!"
    await ctx.send(msg.format(ctx.message.mentions[0].name))

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


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
