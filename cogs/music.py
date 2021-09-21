from asyncio.queues import Queue
import discord
import os
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
import youtube_dl
import asyncio
import pafy


class Music(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)
    
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info ["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            return await ctx.send("Belom masuk voice oy")
        
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        
        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice.client.disconnect()

        await ctx.send("Gw kagak ada di voice channel")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("Masukin lagunya dulu bray")
        
        if ctx.voice_client is None:
            return await ctx.send("Gw mesti ada di channel buat play")

        if not ("youtube.com/watch?" in song or "https://youtub.be/" in song):
            await ctx.send("Mencari lagu....")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Ganemu lagunya cok")

            song = result[0]
        
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Gw lagi muter lagu, lagunya udah di masukin queue: {queue_len+1}")

            else:
                return await ctx.send("Cuman bisa queue 10 lagu doang bos, tunggu lagunya abis ye")
        
        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("Lupa buat masukin lagu buat lagu")

        await ctx.send("Lagi nyari lagu....")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f" Hasil dari '{song}':", description= "Bisa pake URL ini untuk memainkan lagu ini")

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Memunculkan hasil {amount} pertama")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def queue(self,ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Lagi gaada lagu di antrian cuy")
        
        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text=" ")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("Aing lagi kagak play lagu oy")
        
        if ctx.author.voice is None:
            return await ctx.send("Lau kagak ada di voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Gw lagi kagak masang lagu buat lau woy")

        poll = discord.Embed(title=f"Voting skip lagu si {ctx.author.name}={ctx.author.discriminator}", description="**Bates voting ampe 80% yang vote skip**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Lanjut", value=":no_entry_sign:")
        poll.set_footer(text="Voting beres 15 detik")

        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")
        await poll_msg.add_reaction(u"\U0001F6AB")

        await asyncio.sleep(15)

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reaction:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_vlient.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:
                skip = True
                embed = discord.Embed(title="Skip berhasil", description="***Voting buat skip lagu tercapai, ganggu kuping sih keknya***", colour=discord.Colour.dark_blue())
        
        if not skip:
            embed = discord.Embed(title="Skip gagal", description="*Voting buat skip lagunya gagal*\n\n**Voting gagal, minimal voting masuk 80%**", colour=discord.Colour.dark_blue())
        
        embed.set_footer(text="Voting beres")

        await poll_msg.clear_reaction()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)

def setup(bot):
    bot.add_cog(Music(bot))