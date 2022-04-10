import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import sys
import random
import sqlite3
import json
import aiohttp
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.messages = True
intents.typing = False
intents.presences = False
initial_extensions = ['cogs.sql', 'cogs.cards', 'cogs.game', 'cogs.dm', 'cogs.test']

class SKBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', case_insensitive=True, intents=intents)
        self.initial_extensions = [
            'cogs.sql',
            'cogs.cards',
            'cogs.game',
            'cogs.dm',
            'cogs.test'
        ]

    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')

    async def on_ready(self):
        print('I am a shitty bot and I am online meow.')

bot = SKBot()

tokenfile = open('secret.json')
secret = json.load(tokenfile)
bot.run(secret['token'])

@bot.command()
async def character_card(ctx):
    embed = discord.Embed(title="Kill Kat", colour=discord.Colour(0x439b32), description="```\nKill Kat, a cat that kills.```")
    embed.set_image(url=f"{ctx.author.avatar_url}")
    embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
    embed.set_author(name=f"{ctx.author}")
    embed.add_field(name="**Brawn**", value="10", inline=True)
    embed.add_field(name="**Intelligence**", value="10", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def reload_cogs(ctx):
    for extensions in initial_extensions:
        try:
            bot.unload_extension(extensions)
        except Exception as e:
            print(f'Failed to load extension {extensions}', file=sys.stderr)
            traceback.print_exc()
            await ctx.send(f"hehe got some errors")
    for extensions in initial_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            print(f'Failed to load extension {extensions}', file=sys.stderr)
            traceback.print_exc()
            await ctx.send(f"hehe got some errors")
    await ctx.send(f"cogs reloaded")

@bot.command()
async def cmds(ctx):
    embed = discord.Embed(title="Command List", colour=discord.Colour(0x439b32), description="```\n!newplayer CharacterName \n - This command you need to run first, so you can be added to the DB \n!player_deck \n - Shows your current deck\n!pull # \n - Pulls cards from you deck, requires you to be in the DB\n!deck \n - Refreshes your deck\n!hero_points \n - Lists your available Hero Points```")
    await ctx.send(embed=embed)