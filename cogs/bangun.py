import discord
from discord.ext import commands

class Bangun(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def bangunin(self, ctx, target: discord.Member):
		await ctx.send(target.mention + ' woy bangun woy')

def setup(client):
	client.add_cog(Bangun(client))