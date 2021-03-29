import discord
import os
import random

client = discord.Client()

janken_input = ["$batu", "$Batu" , "$kertas", "$Kertas", "$gunting", "$Gunting"]


def janken():
	janken_actions = ["Batu", "Gunting", "Kertas"]

	janken_start = random.choice(janken_actions)
	return janken_start

@client.event
async def on_ready():
	print('We have loggedd in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if any(choice in message.content for choice in janken_input):
		janken_start = janken()
		await message.channel.send(janken_start)
		
		if janken_input == ("$batu") and ("$Batu"):
			if janken_start == ("Batu"):
				await message.channel.send('\n Seri bray')
			elif janken_start == ("Gunting"):
				await message.channel.send('\n Mantap menang boss')
			else:
				await message.channel.send('\n Lah kalah sama bot')

client.run('ODI1NTc3ODQ2NDk0ODU1MTk4.YF_9SQ.5Z_lzncICXaLDOA9Tdo05-dDG54') 

