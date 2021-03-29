import discord
from discord.ext import commands

class Bangun(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def bangunin(self, ctx, target: discord_Member):
		await client.say(target.mention + 'woy bangun woy')