import discord
from discord.ext import commands
from datetime import datetime

from NHentai import NHentai

class cat_nhentai(commands.Cog, name="NHentai Commands"):
    """Documentation"""

    def __init__(self, bot):
        self.bot = bot
        self.nhentai = NHentai()

    @commands.command(name="nh_find", help="find doujin from nhentai")
    async def nh_find(self, ctx, arg):
        print(f"[{datetime.now()}] Command Issued: nh_find\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        if arg.isnumeric():
            await self.nh_display(ctx, arg)
            return
        SearchPage = self.nhentai.search(query=arg, sort='popular', page=1)
        count = 3 if SearchPage.total_results > 3 else SearchPage.total_results
        if count == 0:
            await ctx.send(f"no results were found!")
            return
        embeds = []*count
        i = 0
        while i < count:
            await self.nh_display(ctx, SearchPage.doujins[i].id)
            i+=1

    @commands.command(name="nh_display", help="display doujin from nhentai")
    async def nh_display(self, ctx, arg):
        print(f"[{datetime.now()}] Command Issued: nh_display\n   - message: {ctx.message.content}\n   - debug: {ctx.message}")
        Doujin = self.nhentai._get_doujin(id=arg)
        if Doujin is None:
            await ctx.send(f"no results were found!")
            return
        tags = ""
        for tag in Doujin.tags:
            tags += f"{tag} "
        embed = discord.Embed(
            title=Doujin.title,
            description=Doujin.secondary_title,
            color=discord.Color.gold(),
            url=f"https://nhentai.net/g/{arg}",
        )
        embed.set_image(url=Doujin.images[0])
        embed.add_field(name="Tags", value=tags, inline=True)
        embed.add_field(name="Pages", value=Doujin.total_pages, inline=False)
        embed.set_footer(text=f"Magic code: {arg}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cat_nhentai(bot))