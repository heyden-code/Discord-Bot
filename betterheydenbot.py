import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODI1NTc3ODQ2NDk0ODU1MTk4.YF_9SQ.5Z_lzncICXaLDOA9Tdo05-dDG54')