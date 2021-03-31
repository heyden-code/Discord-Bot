import discord
import os
from discord.ext import commands
import random


class Random(commands.Cog):

	def __init__(self,client):
		self.client = client

	@commands.command()
	async def pilih(self, ctx, *pilihan):
		terpilih = random.choice(pilihan)
		terpilih = terpilih.replace('-', ' ')

		await ctx.send(terpilih)






def setup(client):
	client.add_cog(Random(client))
