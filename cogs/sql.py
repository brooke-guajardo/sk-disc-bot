import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random

class SqlCog(commands.Cog, name='SQL'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        db = sqlite3.connect('space_kings.sqlite3')
        cursor = db.cursor()
        cursor.execute(f"SELECT player_name FROM players")
        print(ctx.author.display_name)
        result = cursor.fetchall()
        if result is None:
            # if we can't find our player we could add them here
            print("SQL no work.")
            await ctx.send(f"SQL no work, git gud.")
        else:
            await ctx.send(result)
        
    @commands.command()
    async def players(self, ctx, arg1):
        db = sqlite3.connect('space_kings.sqlite3')
        cursor = db.cursor()
        ply = (arg1,)
        sql_stuff = """SELECT * FROM players where player_name=? """
        cursor.execute(sql_stuff, ply)
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
        # Gold Deck
        dek = ['Joker', 'Joker', 'King of Clubs', 'Queen of Clubs', 'Jack of Clubs', '10 of Clubs', '9 of Clubs', '8 of Clubs', '7 of Clubs', '6 of Clubs', '5 of Clubs', '4 of Clubs', '3 of Clubs', '2 of Clubs', 'Ace of Clubs', 'King of Spades', 'Queen of Spades', 'Jack of Spades', '10 of Spades', '9 of Spades', '8 of Spades', '7 of Spades', '6 of Spades', '5 of Spades', '4 of Spades', '3 of Spades', '2 of Spades', 'Ace of Spades', 'King of Diamonds', 'Queen of Diamonds', 'Jack of Diamonds', '10 of Diamonds', '9 of Diamonds', '8 of Diamonds', '7 of Diamonds', '6 of Diamonds', '5 of Diamonds', '4 of Diamonds', '3 of Diamonds', '2 of Diamonds', 'Ace of Diamonds', 'King of Hearts', 'Queen of Hearts', 'Jack of Hearts', '10 of Hearts', '9 of Hearts', '8 of Hearts', '7 of Hearts', '6 of Hearts', '5 of Hearts', '4 of Hearts', '3 of Hearts', '2 of Hearts', 'Ace of Hearts']
        # shuffle new deck, deck has 52 standard cards + 2 jokers
        dek = random.shuffle(dek, random.seed())
        # turn array into string to insert
        dek_str = ', '.join(str(e) for e in dek)
        plyr_ins = (arg1, dek_str, ctx.author.display_name,)
        print("New Player Name: ", arg1)
        print("Discord Handle:  ", ctx.author.display_name)
        print("New Deck:        ")
        try:
            # try to insert player discord name and name of character they pass
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            sql_stuff = """INSERT INTO players (player_name, player_deck, player_discord) VALUES (?,?,?)"""
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

    @commands.command()
    async def new_character(self, ctx, arg1, arg2):
        if arg2 is None:
            await ctx.send(f"Please put player name then character name in that order. Ex !new_character Bruce Batman")
        # player_count + 1 is the new player's id
        plyr_ins = (arg2,)
        print("New Player Character Name: ", arg2)
        try:
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            sql_stuff = """INSERT INTO characters (char_name) VALUES (?) """
            ins.execute(sql_stuff, plyr_ins)
        except:
            await ctx.send(f"Character name already in use.")
        db3.commit()
        print("1 new player row inserted, ID: ", ins.lastrowid)
        if ins.lastrowid is None:
            print(f"Name was not inserted, unique contraint error")
        else:
            await ctx.send(f"Name not taken. Adding to DB")


def setup(bot):
    bot.add_cog(SqlCog(bot))
    print('SQL Cog is loaded.')
