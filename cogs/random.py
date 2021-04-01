import discord
import os
from discord.ext import commands
import random

jawaban = [
            'Pasti banget bray gila',
            'Yoi bet bray',
            'Kata gw iya sih',
            'Bener bet lu',
            'Sangat betuul',
            'wadu gatau gw sih kalo itu',
            'Hmmmm... gayakin sih gw',
            'Kayaknya nggak deh',
            'Kata gw nggak sih',
            'Jangan ngarep lah',
            'Menurut gw sih nggak',
            'Nggak. FIX'
            ]


class Random(commands.Cog):

	def __init__(self,client):
		self.client = client

	@commands.command()
	async def pilih(self, ctx, *pilihan):
		terpilih = random.choice(pilihan)
		terpilih = terpilih.replace('-', ' ')

		await ctx.send(terpilih)
		
	@commands.command()
	async def ask(self, ctx, *tanya):
		jawabr = random.choice(jawaban)
		
		await ctx.send(jawabr)






def setup(client):
	client.add_cog(Random(client))
