from types import MethodWrapperType
import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import sys
import random


def create_conn():
    conn = None
    try:
        conn = sqlite3.connect('space_kings.sqlite3')
        print("Connected to the DB.")
    except sqlite3.Error as e:
        print(e)
       
    cursor = conn.cursor()
    return cursor

async def commit_close_conn(cursor):
    await cursor.commit()
    await cursor.close()
    print("Disconnected from the DB.")
