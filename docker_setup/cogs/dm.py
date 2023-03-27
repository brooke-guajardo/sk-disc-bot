import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random
from .sksetup import create_conn, commit_close_conn, commit_conn


class DmCog(commands.Cog, name='DM'):
    def __init__(self, bot):
        self.bot = bot

#######
### The significance of this cog is to limit use to users with the DM flag
### i.e. all of these functions will check for that flag before running
### Need to just add DM check function, instead of checking it everywhere
#######

# set hero points
    @commands.command()
    async def set_hero_points(self, ctx, arg1, arg2):
        x = int(arg2)
        # is player a 'DM' ?, we check with author's display name
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dm
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to query if {ctx.author.display_name} is a DM, tell JardoRook to git gud.")
            await ctx.send("Syntax is !set_hero_points CharacterName number")
        result = cursor.fetchone()
        commit_close_conn(conn)
        # if flag = 1, author is a DM, if 0, they are not.
        if int(result[0]) != 1:
            # author is no DM! get outta here!
            await ctx.send(f"{ctx.author.display_name} you are not an authorized DM. Git Rekt.")
        else:
            # author is a DM!
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                plyr_ins = (x, arg1,)
                sql_stuff = """
                    UPDATE players
                    SET player_hero_points = (?)
                    WHERE player_name = (?)"""
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to update hero points, :( guess you're no hero.")
            await ctx.send("Hero Points have been updated to %d" %x)

# set player attributes points
    @commands.command()
    async def set_attr_points(self, ctx, arg1, arg2, arg3):
        # arg1 - character name
        # arg2 - attribute
        # arg3 - number
        # is player a 'DM' ?, we check with author's display name
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dm
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to query if {ctx.author.display_name} is a DM, tell JardoRook to git gud.")
            await ctx.send("Syntax is !set_hero_points CharacterName number")
        result = cursor.fetchone()
        commit_close_conn(conn)
        # if flag = 1, author is a DM, if 0, they are not.
        if int(result[0]) != 1:
            # author is no DM! get outta here!
            await ctx.send(f"{ctx.author.display_name} you are not an authorized DM. Git Rekt.")
        else:
            x = int(arg3)
            plyr_ins = (x, arg1,)
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                # + arg1 + allows us to alias the column so I don't fucking make 6 elif's smh
                sql_stuff = 'UPDATE players SET player_'+arg2+' = (?) WHERE player_name = (?)'
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to update attribute, :( guess you're not allowed.")
            await ctx.send(f"Attribute {arg2} updated to {x} for {arg1}.")

# reset dodge and drive after a session/encounter
    @commands.command()
    async def session(self, ctx):
        # resetting for all players... totally not a bad thing to do lol eks dee
        # is player a 'DM' ?, we check with author's display name
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dm
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to query if {ctx.author.display_name} is a DM, tell JardoRook to git gud.")
            await ctx.send("Syntax is !set_hero_points CharacterName number")
        result = ins.fetchone()
        commit_close_conn(conn)
        # if flag = 1, author is a DM, if 0, they are not.
        if int(result[0]) != 1:
            # author is no DM! get outta here!
            await ctx.send(f"{ctx.author.display_name} you are not an authorized DM. Git Rekt.")
        else:
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                # + arg1 + allows us to alias the column so I don't fucking make 6 elif's smh
                sql_stuff = 'update players set player_drive=player_wit + player_presence'
                ins_cursor.execute(sql_stuff,)
                commit_conn(conn)
                sql_stuff = 'update players set player_dodge=player_wit + player_agility - 2'
                ins.execute(sql_stuff,)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to reset drive, :( guess you're not allowed.")
            await ctx.send("Drive and Dodge reset")

# take damage, need to be DM, and pass player name and num
    @commands.command()
    async def damage(self, ctx, arg1, arg2):
        # agr1 - Character Name
        # arg2 - dmg/number
        # get fooked, taking damage
        # need to know if the player has enough health to steal
        x = int(arg2)

        # is player a 'DM' ?, we check with author's display name
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dm
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to query if {ctx.author.display_name} is a DM, tell Jardo Rook to git gud.")
            await ctx.send("Syntax is !set_hero_points CharacterName number")
        result = cursor.fetchone()
        commit_close_conn(conn)
        # if flag = 1, author is a DM, if 0, they are not.
        if int(result[0]) != 1:
            # author is no DM! get outta here!
            await ctx.send(f"{ctx.author.display_name} you are not an authorized DM. Git Rekt.")
        else:
            try:
                # try to select player discord name and name of character they pass
                conn, cursor = create_conn()
                plyr_ins = (arg1,)
                sql_stuff = """
                    SELECT player_current_health
                    FROM players
                    WHERE player_name = ?"""
                cursor.execute(sql_stuff, plyr_ins)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to grab current health, tell Jardo Rook to git gud.")
            result = cursor.fetchall()[0]
            commit_close_conn(conn)
            # need to now subtract from total health, its not infinite!
            y = result[0] - x
            # see if the player has enough health to lose any ;)
            if y > 0:
                # we are good enuff
                try:
                    # try to insert player discord name and name of character they pass
                    conn, ins_cursor = create_conn()
                    plyr_ins = (y, arg1,)
                    sql_stuff = """
                        UPDATE players
                        SET player_current_health = (?)
                        WHERE player_name = (?)"""
                    ins_cursor.execute(sql_stuff, plyr_ins)
                    commit_close_conn(conn)
                except sqlite3.Error as e:
                    print(e)
                    await ctx.send(f"ERROR: Unable to update health, this is Jardo Rook's fault.")
                await ctx.send(f"{arg1} has taken damage! Health is now at {y}")
            elif y==0:
                # lmaoooo you ded
                try:
                    # try to insert player discord name and name of character they pass
                    conn, ins_cursor = create_conn()
                    plyr_ins = (y, arg1,)
                    sql_stuff = """
                        UPDATE players
                        SET player_current_health = (?)
                        WHERE player_name = (?)"""
                    ins_cursor.execute(sql_stuff, plyr_ins)
                    commit_close_conn(conn)
                except sqlite3.Error as e:
                    print(e)
                    await ctx.send(f"ERROR: Unable to update health, this is Jardo Rook's fault.")
                await ctx.send(f"You have 0 health. Is this the end for poor {arg1}?")
            else:
                # we are not gucci, feel bad.
                try:
                    # try to insert player discord name and name of character they pass
                    conn, ins_cursor = create_conn()
                    plyr_ins = (0, arg1,)
                    sql_stuff = """
                        UPDATE players
                        SET player_current_health = (?)
                        WHERE player_name = (?)"""
                    ins_cursor.execute(sql_stuff, plyr_ins)
                    commit_close_conn(conn)
                except sqlite3.Error as e:
                    print(e)
                    await ctx.send(f"ERROR: Unable to update health, this is Jardo Rook's fault.")
                await ctx.send(f"{arg1}'s health fell below 0, is that even possible??")

# set player skills
    @commands.command()
    async def set_skill_points(self, ctx, arg1, arg2, arg3):
        # arg1 - character name
        # arg2 - skill
        # arg3 - number
        # is player a 'DM' ?, we check with author's display name
        try:
            conn, cursor = create_conn()
            plyr_ins = (ctx.author.display_name,)
            sql_stuff = """
                SELECT player_dm
                FROM players
                WHERE player_discord = ?"""
            cursor.execute(sql_stuff, plyr_ins)
        except sqlite3.Error as e:
            print(e)
            await ctx.send(f"ERROR: Unable to query if {ctx.author.display_name} is a DM, tell JardoRook to git gud.")
            await ctx.send("Syntax is !set_hero_points CharacterName number")
        result = cursor.fetchone()
        commit_close_conn(conn)
        # if flag = 1, author is a DM, if 0, they are not.
        if int(result[0]) != 1:
            # author is no DM! get outta here!
            await ctx.send(f"{ctx.author.display_name} you are not an authorized DM. Git Rekt.")
        else:
            x = int(arg3)
            plyr_ins = (x, arg1,)
            try:
                # try to insert player discord name and name of character they pass
                conn, ins_cursor = create_conn()
                # + arg1 + allows us to alias the column so I don't fucking make 6 elif's smh
                sql_stuff = f"UPDATE skills SET {arg2}=? WHERE skills_player_id in (select player_id from players where player_name=?)"
                ins_cursor.execute(sql_stuff, plyr_ins)
                commit_close_conn(conn)
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"ERROR: Unable to update skill, :( guess you're not allowed.")
            await ctx.send(f"Skill {arg2} updated to {x} for {arg1}.")

async def setup(bot):
    await bot.add_cog(DmCog(bot))
    print('DM Cog is loaded.')
