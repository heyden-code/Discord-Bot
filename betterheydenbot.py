import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix = '$')

client.lava_nodes = [
	{
		'host' : 'lava.link',
		'port' : 80,
		'rest_uri' : f'http://lava.link:80',
		'identifier' : 'MAIN',
		'password' : 'anything',
		'region' : 'singapore'
	}
]

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	client.load_extension('dismusic')


@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
