import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random


class CardsCog(commands.Cog, name='Cards'):

    def __init__(self, bot):
        self.bot = bot

# user getting new deck, hard reset
    @commands.command()
    async def deck(self, ctx):
        # Gold Deck
        dek = ['Joker', 'Joker', 'King of Clubs', 'Queen of Clubs', 'Jack of Clubs', '10 of Clubs', '9 of Clubs', '8 of Clubs', '7 of Clubs', '6 of Clubs', '5 of Clubs', '4 of Clubs', '3 of Clubs', '2 of Clubs', 'Ace of Clubs', 'King of Spades', 'Queen of Spades', 'Jack of Spades', '10 of Spades', '9 of Spades', '8 of Spades', '7 of Spades', '6 of Spades', '5 of Spades', '4 of Spades', '3 of Spades', '2 of Spades', 'Ace of Spades', 'King of Diamonds', 'Queen of Diamonds', 'Jack of Diamonds', '10 of Diamonds', '9 of Diamonds', '8 of Diamonds', '7 of Diamonds', '6 of Diamonds', '5 of Diamonds', '4 of Diamonds', '3 of Diamonds', '2 of Diamonds', 'Ace of Diamonds', 'King of Hearts', 'Queen of Hearts', 'Jack of Hearts', '10 of Hearts', '9 of Hearts', '8 of Hearts', '7 of Hearts', '6 of Hearts', '5 of Hearts', '4 of Hearts', '3 of Hearts', '2 of Hearts', 'Ace of Hearts']

        # shuffle new deck, deck has 52 standard cards + 2 jokers
        random.shuffle(dek, random.seed())
        print(dek)

        dek_str_for_db = ', '.join(str(e) for e in dek)

        dek_ins = (dek_str_for_db, ctx.author.display_name,)
        print(dek_ins)
        # try to insert deck for player
        try:
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            sql_stuff = """
            UPDATE players
            SET player_deck = (?)
            WHERE player_discord = (?)"""
            ins.execute(sql_stuff, dek_ins)
            db3.commit()
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Someshit happened when inserting your deck into the DB, @JardoRook fix yo shit")
        print("1 new deck row updated, ID: ", ins.lastrowid)
        await ctx.send("A new deck has been added for you.")

# users pulling cards
    @commands.command()
    async def pull(self, ctx, arg1):
        # use discord display name as key to get the player's deck
        db3 = sqlite3.connect('space_kings.sqlite3')
        ins = db3.cursor()
        plyr_ins = (ctx.author.display_name,)
        sql_stuff = """
                SELECT player_deck
                FROM players
                WHERE player_discord= ?
                """
        ins.execute(sql_stuff, plyr_ins)
        # get raw string of current result/deck from query
        result = ins.fetchone()[0]
        if result is None:
            # Player not in DB
            await ctx.send(f"You are not in the DB, please add yourself with !newplayer CharacterName")
            return
        elif result is not None:
            # Player is in DB, lets goooooo
            # Use commas to delimit raw string into an array
            dek_list = result.split(", ")

            # check to make sure they have enough cards to pull
            # check current deck size prior to pulling cards
            deck_size = len(dek_list)

            # get number of cards that user is trying to pull, need to cast string into an int variable
            x = int(arg1)
            y = range(x)

            if deck_size > x:
                # deck has enough cards no issues
                # take off the top of the list
                # create hand
                hand_str = []
                # pull cards with the amount given from command, !pull # where x = #
                for i in y:
                    hand_str.append(dek_list.pop(0))
                # hand_str is the array of strings of the cards the player pulled
                # now to return deck to DB minus the cards we pulled
                # turn array into string to insert
                dek_str_for_db = ', '.join(str(e) for e in dek_list)

                # create update variables
                deck_ins = (dek_str_for_db, ctx.author.display_name,)
                sql_stuff_ins = """
                UPDATE players
                SET player_deck = ?
                WHERE player_discord = ?
                """
                ins.execute(sql_stuff_ins, deck_ins)
                db3.commit()
            else:
                # deck does not have enough cards
                await ctx.send(f"Your deck ran out! Shuffling a new deck")

                # Gold Deck
                dek = ['Joker', 'Joker', 'King of Clubs', 'Queen of Clubs', 'Jack of Clubs', '10 of Clubs', '9 of Clubs', '8 of Clubs', '7 of Clubs', '6 of Clubs', '5 of Clubs', '4 of Clubs', '3 of Clubs', '2 of Clubs', 'Ace of Clubs', 'King of Spades', 'Queen of Spades', 'Jack of Spades', '10 of Spades', '9 of Spades', '8 of Spades', '7 of Spades', '6 of Spades', '5 of Spades', '4 of Spades', '3 of Spades', '2 of Spades', 'Ace of Spades', 'King of Diamonds', 'Queen of Diamonds', 'Jack of Diamonds', '10 of Diamonds', '9 of Diamonds', '8 of Diamonds', '7 of Diamonds', '6 of Diamonds', '5 of Diamonds', '4 of Diamonds', '3 of Diamonds', '2 of Diamonds', 'Ace of Diamonds', 'King of Hearts', 'Queen of Hearts', 'Jack of Hearts', '10 of Hearts', '9 of Hearts', '8 of Hearts', '7 of Hearts', '6 of Hearts', '5 of Hearts', '4 of Hearts', '3 of Hearts', '2 of Hearts', 'Ace of Hearts']

                # shuffle new deck, deck has 52 standard cards + 2 jokers
                random.shuffle(dek, random.seed())

                # we need to pull remaining cards from old deck, and then pull from new deck
                hand_str = []
                it = deck_size
                while it > 0:
                    # pull remaining cards
                    hand_str.append(dek_list.pop(0))
                    it -= 1

                # after loop old deck is spent, get remaining value of cards to pull
                it = range(x - deck_size)

                # pull from new deck that's shuffled
                for i in it:
                    hand_str.append(dek.pop(0))

                # update user's deck with new deck
                dek_str_for_db = ', '.join(str(e) for e in dek)

                # create update variables
                deck_ins = (dek_str_for_db, ctx.author.display_name,)
                sql_stuff_ins = """
                UPDATE players
                SET player_deck = ?
                WHERE player_discord = ?
                """
                ins.execute(sql_stuff_ins, deck_ins)

        db3.commit()

        await ctx.send(hand_str)
        if any("Queen of Hearts" in s for s in hand_str):
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = 'SELECT player_charm FROM players where player_discord= ?'
            ins.execute(sql_stuff, plyr_ins)
            result = ins.fetchall()[0]
            x = result[0] + 1
            # Queen of <3 times crit + 1
            await ctx.send(f"Critical Hit! + {x} Successes!")
        print(hand_str)

# show deck
    @commands.command()
    async def player_deck(self, ctx):
        # use discord display name as key to get the player's deck
        plyr_ins = (ctx.author.display_name,)
        try:
            # pull string from table
            db3 = sqlite3.connect('space_kings.sqlite3')
            ins = db3.cursor()
            sql_stuff = """SELECT player_deck from players where player_discord=?"""
            ins.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: ")
        result = ins.fetchone()[0]
        await ctx.send(result)

async def setup(bot):
    await bot.add_cog(CardsCog(bot))
    print('Cards Cog is loaded.')