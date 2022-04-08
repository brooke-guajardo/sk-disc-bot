import discord
from discord.ext import commands
import asyncio
import datetime
import sys
import random
import sqlite3
import json

bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
    print('I am a shitty bot and I am online meow.')

# extensions
initial_extensions = ['cogs.sql', 'cogs.cards', 'cogs.game']

# main
if __name__ == '__main__':
    for extensions in initial_extensions:
        try:
            bot.load_extension(extensions)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()

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
async def commands(ctx):
    embed = discord.Embed(title="Command List", colour=discord.Colour(0x439b32), description="```\n!newplayer CharacterName \n - This command you need to run first, so you can be added to the DB \n!player_deck \n - Shows your current deck\n!pull # \n - Pulls cards from you deck, requires you to be in the DB\n!deck \n - Refreshes your deck\n!hero_points \n - Lists your available Hero Points```")
    await ctx.send(embed=embed)

# Pass the token
tokenfile = open('secret.json')
secret = json.load(tokenfile)
bot.run(secret['token'])
