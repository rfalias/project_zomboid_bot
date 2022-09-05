#!/usr/bin/env python3
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import socket
import asyncio
from concurrent.futures import ThreadPoolExecutor
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from subprocess import Popen
import glob
import subprocess
from file_read_backwards import FileReadBackwards
import datetime
# Setup environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LOG_PATH = os.getenv('LOG_PATH', "/home/steam/Zomboid/Logs")
NOTIFICATION_CHANNEL = os.getenv('NOTIFICATION_CHANNEL')
INGAME_CHANNEL = os.getenv('INGAME_CHANNEL')
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
access_levels = ['admin', 'none', 'moderator']
client = discord.Client(intents=intents)


import asyncio
from watchgod import awatch


async def logwatcher():
    await client.wait_until_ready()
    counter = 0
    nchannel = client.get_channel(id=int(NOTIFICATION_CHANNEL))
    ichannel = client.get_channel(id=int(INGAME_CHANNEL))
    async for changes in awatch(LOG_PATH):
        found_files = list()
        for p in changes:
            found_files.append(p[1])
        user_paths = list(filter(lambda x: "_user.txt" in x, found_files))
        for x in user_paths:
            print(f"Checking {x} for deaths and player join")
            player_check = await PlayerCheck(x, nchannel)



player_notif = {}
async def PlayerCheck(lfile, channel):
    count = 0
    try:
        with FileReadBackwards(lfile) as frb:
            for l in frb:
                if "disconnected player" in l:
                    if count == 0:
                        count += 1
                        continue
                ls = l.split()
                if "removed connection index" in l:
                    user = ls[3].strip('"')
                    player_notif[user] = 0
                    await channel.send(f"{user} has disconnected!")
                    break
                if "fully connected (" in l:
                    user = ls[3].strip('"')
                    if player_notif.get(user, 0) < 1:
                        print("Send join")
                        await channel.send(f"{user} has joined!")
                    else:
                        player_notif[user] -= 1

                    break
                if "died at (" in l:
                    if count > 0:
                        break
                    user = ls[3].strip('"')
                    player_notif[user] = 1
                    await channel.send(f"{user} has died!")
                    break
                break
    except Exception as e:
        print(e)



async def IsAdmin(ctx):
    is_present = [i for i in ctx.author.roles if i.name in ADMIN_ROLES]
    return is_present



client.loop.create_task(logwatcher())
client.run(TOKEN)
