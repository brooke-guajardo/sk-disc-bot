import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random


class GameCog(commands.Cog, name='Game'):

    def __init__(self, bot):
        self.bot = bot

# see hero points
    @commands.command()
    async def hero_points(self, ctx):
        try:
            # try to select player discord name and name of character they pass
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_hero_points
                FROM players
                WHERE player_discord = ?"""
            ins.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab hero points, :( guess you're no hero.")
        result = ins.fetchone()[0]
        await ctx.send(result)

# set hero points
    @commands.command()
    async def set_hero_points(self, ctx, arg1, arg2):
        x = int(arg1)
        if ctx.author.display_name == 'JardoRook' and isinstance(x, int):
            try:
                # try to insert player discord name and name of character they pass
                db3 = sqlite3.connect('space_kings.sqlite3')
                ins = db3.cursor()
                plyr_ins = (x, arg2,)
                sql_stuff = """
                    UPDATE players
                    SET player_hero_points = (?)
                    WHERE player_discord = (?)"""
                ins.execute(sql_stuff, plyr_ins)
                db3.commit()
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab hero points, :( guess you're no hero.")
            await ctx.send("Hero Points have been updated to %d" %x)
        else:
            await ctx.send(f"You are not allowed to edit this param, only the DM can. And the first param needs to be a number")

def setup(bot):
    bot.add_cog(GameCog(bot))
    print('Game Cog is loaded.')

