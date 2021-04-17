import discord
from discord.ext import commands
from datetime import datetime

class cat_debug(commands.Cog, name="Debug commands"):
    """Documentation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tell_me_about_yourself(self, ctx):
        print(f"[{datetime.now()}] Command Issued: tell_me_about_yourself\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        text = "My name is OnikenX's pet!\n I was built originally by Kakarot2000. I'm now ~~a slave to OnikenX~~ OnikenX's loyal pet, you can see my services with !help.\n :)"
        await ctx.send(text)

    @commands.command(help="Prints details of Author")
    async def whats_my_name(self, ctx):
        print(f"[{datetime.now()}] Command Issued: whats_my_name\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        await ctx.send(f"Hello {ctx.author.name}")


    @commands.command(help="Prints details of Server")
    async def where_am_i(self, ctx):
        print(f"[{datetime.now()}] Command Issued: where_am_i\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
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
    
def setup(bot):
    bot.add_cog(cat_debug(bot))