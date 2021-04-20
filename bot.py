import discord
import random
import os

from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token") # Get the API token from the .env file.
PREFIX = os.getenv("command_prefix") # Get the command prefix from the .env file.
if PREFIX is None:
    PREFIX = "!" 
print(f"prefix: {PREFIX}")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.load_extension('debug')
bot.load_extension('audio')
bot.load_extension('nhentai')
#bot = discord.Client(intents=intents)


######################################################################
#############################  SAVE   ################################
#############################   AND   ################################
#############################   LOAD  ################################
######################################################################

#TODO

######################################################################
#############################  SAFE   ################################
#############################   FOR   ################################
#############################   WORK  ################################
######################################################################

#TODO

#######################################################################
#############################          ################################
#############################  BATTLE  ################################
#############################          ################################
#######################################################################

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

######################################################################
#############################         ################################
############################# DOILOVE ################################
#############################         ################################
######################################################################

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
    await ctx.send(msg.format(ctx.message.mentions[0].display_name))

##########################################################################
##############################  NORMAL  ##################################
##############################   BOT    ##################################
##############################   STUFF  ##################################
##########################################################################

@bot.event
async def on_ready():
    print("Running!")
    for guild in bot.guilds:
        # for channel in guild.text_channels:
        # if str(channel) == "general":
        # await channel.send("Bot Activated..")
        # await channel.send(file=discord.File("giphy.png"))
        print(f"Active in {guild.name}\n Member Count : {guild.member_count}")

@bot.event
async def on_message(message):
    # bot.process_commands(msg) is a couroutine that must be called here since we are overriding the on_message event
    await bot.process_commands(message)

    ctx = await bot.get_context(message)
    message_string = str(message.content).lower()
    if message_string.find("tetr.io") != -1 or message_string.find("tetris") != -1:
        await message.channel.send("Alguém falou em **T E T R I S**?\n⚡⚡⚡!!!Thunder!!!⚡⚡⚡")
        await add_to_playlist(ctx, "https://www.youtube.com/watch?v=bB-d7bc63CE")

    if message_string in ["swear_word1", "swear_word2"]:
        await message.channel.purge(limit=1)

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

@bot.command(name="cona")
async def cona(ctx):
    await ctx.send(f"Eu só quero {ctx.author.name} 😳")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
