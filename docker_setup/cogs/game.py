import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import datetime
import sqlite3
import sys
import random
from .sksetup import create_conn, commit_close_conn

class GameCog(commands.Cog, name='Game'):
    def __init__(self, bot):
        self.bot = bot

#######
### The significance of this cog is to contain all game mechanic functions
### most will require the author to exist in the sqlite3 db, please reference sql.py newplayer
#######

# see hero points
    @commands.command()
    async def hero_points(self, ctx):
        try:
            # try to select player discord name and name of character they pass
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_hero_points
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab hero points, :( guess you're no hero.")
        result = cursor.fetchone()[0]
        commit_close_conn(conn)
        await ctx.send(result)

# see drive points
    @commands.command()
    async def drive_points(self, ctx):
        try:
            # try to select player discord name and name of character they pass
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_drive
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab drive, :( guess you're not licensed.")
        result = cursor.fetchone()[0]
        commit_close_conn(conn)
        await ctx.send(result)

# set drive points, number then player discord name
    @commands.command()
    async def set_drive_points(self, ctx, arg1, arg2):
        hero_pts = int(arg1)
        # need to add DM flag, or DM role check here
        if ctx.author.display_name == 'JardoRook' and isinstance(hero_pts, int):
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                plyr_ins = (hero_pts, arg2,)
                sql_stuff = """
                    UPDATE players
                    SET player_drive = (?)
                    WHERE player_discord = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab drive points, :( guess you're not licensed.")
            await ctx.send(f"Drive Points have been updated to {hero_pts}")
        else:
            await ctx.send(f"You are not allowed to edit this param, only the DM can. And the first param needs to be a number\nExample: !set_drive_points 3 JardoRook")

# use drive
    @commands.command()
    async def drive(self, ctx, arg1):
        try:
            # try to select player discord name and name of character they pass
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_drive
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab drive, :( guess you're not licensed.")
        result = cursor.fetchone()[0]
        # await ctx.send(result)
        # make arg1 an int, i.e. the amount of drive a player wants to use
        x = int(arg1)
        # need to now subtract from total drive, its not infinite!
        y = result - x
        # see if the player has enough drive to use
        if result - x >=0:
            # we are gucci and we can use dat drive
            await ctx.invoke(self.bot.get_command('pull'), arg1=x)
            try:
                # try to insert player discord name and name of character they pass
                #db3 = sqlite3.connect('space_kings.sqlite3')
                #ins = db3.cursor()
                plyr_ins = (y, ctx.author.display_name,)
                sql_stuff = """
                    UPDATE players
                    SET player_drive = (?)
                    WHERE player_discord = (?)"""
                cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab drive points, :( guess you're not licensed.")
            await ctx.send(f"Drive Points have been updated to {y}")
        else:
            # we are not gucci, feel bad.
            await ctx.send(f"You are trying to use more drive than you have. You currently have: {result}")

# use hero points
    @commands.command()
    async def hero(self, ctx, arg1):
        try:
            # try to select player discord name and name of character they pass
            conn, cursor = create_conn()
            plyr_ins  = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_hero_points
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab hero points, :( guess you're no hero.")
        result = cursor.fetchone()[0]
        commit_close_conn(conn)
        # make arg1 an int, i.e. the amount of drive a player wants to use
        x = int(arg1)
        # need to now subtract from total drive, its not infinite!
        y = result - x
        # see if the player has enough drive to use
        if result - x >=0:
            # we are gucci and we can use dat drive
            await ctx.invoke(self.bot.get_command('pull'), arg1=x*2)
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                plyr_ins  = (y, ctx.author.display_name,)
                sql_stuff = """
                    UPDATE players
                    SET player_hero_points = (?)
                    WHERE player_discord = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab hero points, :( guess you're no hero.")
            await ctx.send(f"Hero Points have been updated to {y}")
        else:
            # we are not gucci, feel bad.
            await ctx.send(f"You are trying to use more hero points than you have. You currently have: {result}")

# character sheet demo - WIP
    @commands.command()
    async def char(self, ctx):
        try:
            conn, cursor = create_conn()
            plyr_ins  = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_brawn, player_intelligence, player_charm, player_agility, player_wit, player_presence, player_name, player_char_desc
                FROM players
                WHERE player_discord= ?
                """
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: ")

        attributes = cursor.fetchone()
        commit_close_conn(conn)

        # need to format results
        brawn        = attributes[0]
        intelligence = attributes[1]
        charm        = attributes[2]
        agility      = attributes[3]
        wit          = attributes[4]
        presence     = attributes[5]
        name         = attributes[6]
        char_desc    = attributes[7]

        # fancy discord embed
        embed = discord.Embed(title=f"{name}", colour=discord.Colour(0x439b32), description=f"```\n{char_desc}```")
        embed.set_author(name=f"{ctx.author}")
        embed.add_field(name="**Brawn**", value=f"{brawn}", inline=True)
        embed.add_field(name="**Intelligence**", value=f"{intelligence}", inline=True)
        embed.add_field(name="**Charm**", value=f"{charm}", inline=True)
        embed.add_field(name="**Agility**", value=f"{agility}", inline=True)
        embed.add_field(name="**Wit**", value=f"{wit}", inline=True)
        embed.add_field(name="**Presence**", value=f"{presence}", inline=True)
        embed.set_thumbnail(url=f"{ctx.author.avatar.url}")
        await ctx.send(embed=embed)

# list out player attributes
    @commands.command()
    async def list_attr(self, ctx):
        try:
            conn, cursor = create_conn()
            plyr_ins  = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_brawn, player_intelligence, player_charm, player_agility, player_wit, player_presence, player_name
                FROM players
                WHERE player_discord= ?
                """
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: ")

        attributes = cursor.fetchone()
        commit_close_conn(conn)

        # need to format results
        brawn        = attributes[0]
        intelligence = attributes[1]
        charm        = attributes[2]
        agility      = attributes[3]
        wit          = attributes[4]
        presence     = attributes[5]
        name         = attributes[6]

        # fancy discord embed
        embed = discord.Embed(colour=discord.Colour(0x439b32))
        embed.set_author(name=f"{name}")
        embed.add_field(name="**Brawn**", value=f"{brawn}", inline=True)
        embed.add_field(name="**Intelligence**", value=f"{intelligence}", inline=True)
        embed.add_field(name="**Charm**", value=f"{charm}", inline=True)
        embed.add_field(name="**Agility**", value=f"{agility}", inline=True)
        embed.add_field(name="**Wit**", value=f"{wit}", inline=True)
        embed.add_field(name="**Presence**", value=f"{presence}", inline=True)
        await ctx.send(embed=embed)

# list out player skills
    @commands.command()
    async def list_skills(self, ctx):
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT
                athletics,
                biology,
                computers,
                empathy,
                engineering,
                explosives,
                firearms,
                investigation,
                law,
                lying,
                melee,
                perform,
                piloting,
                persuasion,
                sneaking,
                spacewise,
                survival,
                telekinesis,
                telepathy,
                players.player_name
                FROM skills
                INNER JOIN players
                ON skills.skills_player_id=players.player_id
                WHERE player_discord= ?
                """
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: ")

        skills = cursor.fetchone()
        commit_close_conn(conn)

        # need to format results
        athletics     = skills[0]
        biology       = skills[1]
        computers     = skills[2]
        empathy       = skills[3]
        engineering   = skills[4]
        explosives    = skills[5]
        firearms      = skills[6]
        investigation = skills[7]
        law           = skills[8]
        lying         = skills[9]
        melee         = skills[10]
        perform       = skills[11]
        piloting      = skills[12]
        persuasion    = skills[13]
        sneaking      = skills[14]
        spacewise     = skills[15]
        survival      = skills[16]
        telekinesis   = skills[17]
        telepathy     = skills[18]
        name          = skills[19]

        # fancy discord embed
        embed = discord.Embed(colour=discord.Colour(0x439b32))
        embed.set_author(name=f"{name}")
        embed.add_field(name="**Athletics**", value=f"{athletics}", inline=True)
        embed.add_field(name="**Biology**", value=f"{biology}", inline=True)
        embed.add_field(name="**Computers**", value=f"{computers}", inline=True)
        embed.add_field(name="**Empathy**", value=f"{empathy}", inline=True)
        embed.add_field(name="**Engineering**", value=f"{engineering}", inline=True)
        embed.add_field(name="**Explosives**", value=f"{explosives}", inline=True)
        embed.add_field(name="**Firearms**", value=f"{firearms}", inline=True)
        embed.add_field(name="**Investigation**", value=f"{investigation}", inline=True)
        embed.add_field(name="**Law**", value=f"{law}", inline=True)
        embed.add_field(name="**Lying**", value=f"{lying}", inline=True)
        embed.add_field(name="**Melee**", value=f"{melee}", inline=True)
        embed.add_field(name="**Perform**", value=f"{perform}", inline=True)
        embed.add_field(name="**Piloting**", value=f"{piloting}", inline=True)
        embed.add_field(name="**Persuasion**", value=f"{persuasion}", inline=True)
        embed.add_field(name="**Sneaking**", value=f"{sneaking}", inline=True)
        embed.add_field(name="**Spacewise**", value=f"{spacewise}", inline=True)
        embed.add_field(name="**Survival**", value=f"{survival}", inline=True)
        embed.add_field(name="**Telekinesis**", value=f"{telekinesis}", inline=True)
        embed.add_field(name="**Telepathy**", value=f"{telepathy}", inline=True)
        await ctx.send(embed=embed)

# main player command, player attribute + skills
    @commands.command()
    async def roll(self, ctx, arg1, arg2):
        conn, cursor = create_conn()
        plyr_ins  = (ctx.author.display_name,)
        sql_stuff = 'SELECT skills.'+arg1+', players.player_'+arg2+', player_health, player_brawn, player_current_health FROM skills inner join players on skills.skills_player_id=players.player_id where player_discord= ?'
        cursor.execute(sql_stuff, plyr_ins)
        # get skill and attr results and add them, they're int values already
        result = cursor.fetchall()[0]
        commit_close_conn(conn)
        # calc cards to draw from skill+ attr
        x = result[0] + result[1]
        # is player healthy? compare current health with calculated injury = player_health- player_brawn
        injured = result[2] - result[3]
        current_health = result[4]
        if current_health > injured:
            # player is healthy and can pulll an extra card
            x = x + 1
            # assign x the integer value of attribute + skill + healthy
            await ctx.send(f"Your {arg1} skill is: {result[0]}")
            await ctx.send(f"Your {arg2} attribute is: {result[1]}")
            await ctx.send(f"You\'re healthy! +1 card to pull")
            await ctx.invoke(self.bot.get_command('pull'), arg1=x)
        else:
            # assign x the integer value of attribute + skill
            await ctx.send(f"Your {arg1} skill is: {result[0]}")
            await ctx.send(f"Your {arg2} attribute is: {result[1]}")
            await ctx.invoke(self.bot.get_command('pull'), arg1=x)

# catch phrase!
    @commands.command()
    async def catch_phrase(self, ctx):
        conn, cursor = create_conn()
        plyr_ins  = (ctx.author.display_name,)
        sql_stuff = 'SELECT skills.perform, players.player_charm FROM skills inner join players on skills.skills_player_id=players.player_id where player_discord= ?'
        cursor.execute(sql_stuff, plyr_ins)
        result = cursor.fetchall()[0]
        commit_close_conn(conn)
        x = result[0] + result[1] # charm + persuasion, CATCH PHRASE!
        # assign x the integer value of attribute + skill
        await ctx.invoke(self.bot.get_command('pull'), arg1=x)

# track dodge, i.e. consume it
    @commands.command()
    async def dodge(self, ctx, arg1):
        try:
            # try to select player discord name and name of character they pass
            conn, cursor = create_conn()
            plyr_ins  = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dodge
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to grab dodge, :( pls message JardoRook and tell them to git gud")
        result = cursor.fetchone()[0]
        commit_close_conn(conn)
        # await ctx.send(result)
        # make arg1 an int, i.e. the amount of dodge a player wants to use
        x = int(arg1)
        # need to now subtract from total dodge, its not infinite!
        y = result - x
        # see if the player has enough dodge to use
        if result - x >=0:
            # they have dodge to use
            try:
                # update db with new dodge value
                conn, ins_cursor = create_conn()
                plyr_ins  = (y, ctx.author.display_name,)
                sql_stuff = """
                    UPDATE players
                    SET player_dodge = (?)
                    WHERE player_discord = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab dodge, :( pls message JardoRook and tell them to git gud")
            await ctx.send(f"Dodge has been updated to {y}")
        else:
            # we are not gucci, feel bad.
            await ctx.send(f"You are trying to use more dodge than you have. You currently have: {result}")

# healing
    @commands.command()
    async def heal(self, ctx, arg1, arg2):
        x = int(arg2)
        if ctx.author.display_name == 'JardoRook':
            try:
                # try to select player discord name and name of character they pass
                conn, cursor = create_conn()
                plyr_ins  = (arg1,)
                sql_stuff = """
                    SELECT player_current_health, player_health
                    FROM players
                    WHERE player_name = ?"""
                cursor.execute(sql_stuff, plyr_ins)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab current health, tell JardoRook to git gud.")
        result = cursor.fetchall()[0]
        commit_close_conn(conn)
        # current health + healing
        x = result[0] + x
        if x > result[1]:
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                plyr_ins  = (result[1], arg1,)
                sql_stuff = """
                    UPDATE players
                    SET player_current_health = (?)
                    WHERE player_name = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to update health, this is JardoRook's fault.")
            await ctx.send(f"{arg1}'s health is now full!")
        else:
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                plyr_ins = (x, arg1,)
                sql_stuff = """
                    UPDATE players
                    SET player_current_health = (?)
                    WHERE player_name = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to update health, this is JardoRook's fault.")
            await ctx.send(f"{arg1} got healed! Health is now at {x}")

# stats, list out initiative, dodge, drive and crit
    @commands.command()
    async def status(self, ctx):
        try:
            conn, cursor = create_conn()
            plyr_ins  = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_init, player_dodge, player_drive, player_charm + 1, player_hero_points, player_name, player_current_health, player_brawn
                FROM players
                WHERE player_discord= ?
                """
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: ")

        attributes = cursor.fetchone()
        commit_close_conn(conn)

        # need to format results
        init   = attributes[0]
        dodge  = attributes[1]
        drive  = attributes[2]
        crit   = attributes[3]
        hero   = attributes[4]
        name   = attributes[5]
        health = attributes[6]
        brawn  = attributes[7]

        # fancy discord embed
        embed = discord.Embed(colour=discord.Colour(0x439b32), title="Health")
        embed.set_author(name=f"{name}")
        embed.add_field(name="**Current Health**", value=f"{health}", inline=True)
        embed.add_field(name="**Injured**", value=f"{brawn * 2}", inline=True)
        embed.add_field(name="**Unconscious**", value=f"{brawn}", inline=True)
        await ctx.send(embed=embed)
        embed2 = discord.Embed(colour=discord.Colour(0x439b32), title="Stats")
        embed2.add_field(name="**Initiative**", value=f"{init}", inline=True)
        embed2.add_field(name="**Dodge**", value=f"{dodge}", inline=True)
        embed2.add_field(name="**Drive**", value=f"{drive}", inline=True)
        embed2.add_field(name="**Crit**", value=f"{crit}", inline=True)
        embed2.add_field(name="**Hero Points**", value=f"{hero}", inline=True)
        await ctx.send(embed=embed2)

async def setup(bot):
    await bot.add_cog(GameCog(bot))
    print('Game Cog is loaded.')
