import discord
import random
from discord.ext import commands
from rps.parser import JankenParser
from rps.model import RPS

class Janken(commands.Cog):
	
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def janken(self, ctx, janken_input:JankenParser):

		janken_m = RPS()
		janken_bot = random.choice(janken_m.get_choices())
		janken_input = janken_input.choice

		winner_check = {
			(RPS.BATU, RPS.KERTAS): False,
			(RPS.BATU, RPS.GUNTING): True,
			(RPS.KERTAS, RPS.BATU): True,
			(RPS.KERTAS, RPS.GUNTING): False,
			(RPS.GUNTING, RPS.BATU): False,
			(RPS.GUNTING, RPS.KERTAS): True,
		}

		won = None

		if janken_bot == janken_input:
			won = None
		else:
			won = winner_check[(janken_input,janken_bot)]

		if won is None:
			message = "Seri bray! \n\nlau : %s \naing : %s " %(janken_input, janken_bot)
		elif won is True:
			message = "Mantap menang bray! \n\nlau : %s \naing : %s " %(janken_input, janken_bot)
		elif won is False:
			message = "Yeuu kalah kok sama bot? \n\nlau : %s \naing : %s " %(janken_input, janken_bot)

		await ctx.send(message)

	
def setup(client):
	client.add_cog(Janken(client))