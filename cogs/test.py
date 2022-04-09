import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random

class TestCog(commands.Cog, name='Test'):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def pings(self, ctx):
        await ctx.send(f"Meow meow meow")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestCog(bot))
    print('Test Cog is loaded.')