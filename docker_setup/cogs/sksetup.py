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
        logger.info('Connected to the DB.')
    except sqlite3.Error as e:
        print(e)
        logger.error(e)
       
    cursor = conn.cursor()
    return conn, cursor

def commit_close_conn(conn):
    conn.commit()
    conn.close()
    print("Disconnected from the DB.")
    logger.info('Disconnected from the DB.')

def commit_conn(conn):
    conn.commit()
    print("Committed")
    logger.info('Disconnected from the DB.')
