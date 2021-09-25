import discord
from discord.ext import commands

class Pentung(commands.cog):

    def __init__(self, client):
        self.client = client

        @commands.command()
        async def pentung(self, ctx, target: discord.Member):
            await ctx.send("PRIIIIIIT :U+1F4A5: :U+1F528: HEY "+target.mention)

def setup(client):
    client.add_cog(Pentung(client))