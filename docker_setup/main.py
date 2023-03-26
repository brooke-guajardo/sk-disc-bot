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

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# new swanky intents that I totally don't hurt myself in my confusion over
intents = discord.Intents.all()

# cogs
initial_extensions = ['cogs.sql', 'cogs.cards', 'cogs.game', 'cogs.dm']

class SKBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', case_insensitive=True, intents=intents)
        self.initial_extensions = [
            'cogs.sql',
            'cogs.cards',
            'cogs.game',
            'cogs.dm'
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

