import discord
from discord.ext import commands

class Pentung(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pentung(self, ctx, target: discord.Member):
        await ctx.send(target.mention + "PRIIIIIIT :boom: :hammer: HEY ")

def setup(client):
    client.add_cog(Pentung(client))
