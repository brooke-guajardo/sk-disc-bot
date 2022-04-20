import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random
from sksetup import create_conn, commit_close_conn

class SqlCog(commands.Cog, name='SQL'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        cursor = create_conn()
        #db = sqlite3.connect('space_kings.sqlite3')
        #cursor = db.cursor()
        cursor.execute(f"SELECT player_name FROM players")
        print(ctx.author.display_name)
        result = cursor.fetchone()
        if result is None:
            # if we can't find our player we could add them here
            print("SQL no work.")
            await ctx.send(f"SQL no work, git gud.")
        else:
            await ctx.send(result[0])
        commit_close_conn()

    # will return the character's character_sheet
    @commands.command()
    async def players(self, ctx):
        db = sqlite3.connect('space_kings.sqlite3')
        cursor = db.cursor()
        sql_stuff = """SELECT character_name FROM character_sheet"""
        cursor.execute(sql_stuff,)
        result = cursor.fetchall()
        if result is None:
            # if we can't find our player we could add them here
            print("SQL no work.")
            await ctx.send(f"SQL no work, git gud.")
        else:
            await ctx.send(result)

    # new player command that uses author display name
    @commands.command()
    async def newplayer(self, ctx, arg1):
        # add a new player to the table but using discord handle and gold deck shuffled
        plyr_ins = (arg1, ctx.author.display_name,)
        print("New Player Name: ", arg1)
        print("Discord Handle:  ", ctx.author.display_name)
        try:
            # try to insert player discord name and name of character they pass
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            sql_stuff = """INSERT INTO players (player_name, player_discord) VALUES (?,?)"""
            ins.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: User not added to DB")
        db3.commit()
        print("1 new player row inserted, ID: ", ins.lastrowid)
        if ins.lastrowid is None:
            print(f"User was not inserted, please check the logs")
        else:
            await ctx.send(f"User not found. Adding to DB")
            await ctx.invoke(self.bot.get_command('deck'))

async def setup(bot):
    await bot.add_cog(SqlCog(bot))
    print('SQL Cog is loaded.')