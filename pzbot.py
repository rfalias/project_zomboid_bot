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
from rcon import rcon
from rcon import Client
from subprocess import Popen
import glob
import subprocess
import psutil
import schedule

# Setup environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
RCONPASS = os.getenv('RCON_PASS')
RCONSERVER = os.getenv('RCON_SERVER')
RCONPORT = os.getenv('RCON_PORT')
GUILD = os.getenv('DISCORD_GUILD')
ADMIN_ROLES = os.getenv('ADMIN_ROLES')
LOG_PATH = os.getenv('LOG_PATH', "/home/steam/Zomboid/Logs")
ADMIN_ROLES = ADMIN_ROLES.split(',')
IGNORE_CHANNELS = os.getenv('IGNORE_CHANNELS')
NOTIFICATION_CHANNEL = os.getenv('NOTIFICATION_CHANNEL')
try:
    IGNORE_CHANNELS = IGNORE_CHANNELS.split(',')
except: 
    IGNORE_CHANNELS = ""
bot = commands.Bot(command_prefix='!')
access_levels = ['admin', 'none', 'moderator']
intents = discord.Intents.default()
intents.members = True
block_notified = list()
client = discord.Client()

async def GetDeathCount(ctx, player):
    deathcount = 0
    logs = list()
    for root, dirs, files in os.walk(LOG_PATH):
        for f in files:
            if "_user.txt" in f:
                lpath = os.path.join(root,f)
                logs.append(lpath)
    for log in logs:
        with open(log, 'r') as file:
            for line in file:
                if player.lower() in line.lower():
                    if "died" in line:
                        deathcount += 1
    return f"{player} has died {deathcount} times"


async def IsAdmin(ctx):
    is_present = [i for i in ctx.author.roles if i.name in ADMIN_ROLES]
    return is_present


async def IsServerRunning():
    for proc in psutil.process_iter():
        lname = proc.name().lower()
        if "projectzomboid" in lname:
           return True
    return False


async def rcon_command(ctx, command):
    c = ["/home/steam/pz_bot/rcon", "-a", f"{RCONSERVER}:{RCONPORT}", "-p",RCONPASS, ]
    cmd = [" ".join(command)]
    c.extend(cmd)
    

    print(c)
    p = Popen(c, stdout=subprocess.PIPE)
    r = p.stdout.read()
    r = r.decode("utf-8")
    print(r)
    return r



async def IsChannelAllowed(ctx):
    channel_name = str(ctx.message.channel)
    is_present = [i for i in IGNORE_CHANNELS if i.lower() == channel_name.lower()]
    if channel_name in IGNORE_CHANNELS:
        if channel_name not in block_notified:
            await ctx.send("Not allowed to run commands in this channel")
            block_notified.append(channel_name)
        raise Exception("Not allowed to operate in channel")


class AdminCommands(commands.Cog):
    """Admin Server Commands"""
    @commands.command(pass_context=True)
    async def pzsetaccess(self, ctx): 
        """Set the access level of a specific user."""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            level = ""
            try:
                user = access_split[1]
                access_level = access_split[2]
            except IndexError as ie:
                response = f"Invalid command. Try !pzsetaccess USER ACCESSLEVEL"
                await ctx.send(response)
                return
            if access_level not in access_levels:
                response = f"Invalid access level {level}. Muse be one of {access_levels}"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx, [f"setaccesslevel", f"{user}", f"{access_level}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzsteamban(self, ctx):
        """Steam ban a user"""
        await IsChannelAllowed(ctx)
        if not await IsChannelAllowed(ctx):
            return
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                user = access_split[1]
            except IndexError as ie:
                response = f"Invalid command. Try !pzsteamban USER"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"banid", f"{user}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzsteamunban(self, ctx):
        """Steam unban a user"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                user = access_split[1]
            except IndexError as ie:
                response = f"Invalid command. Try !pzsteamunban USER"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"unbanid", "{user}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzteleport(self, ctx):
        """Teleport a user to another user"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                usera = access_split[1]
                userb = access_split[2]  
            except IndexError as ie:
                response = f"Invalid command. Try !pzteleport USERA to USERB"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"teleport", f"{usera}",f"{userb}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzkick(self, ctx):
        """Kick a user"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                user = access_split[1]
            except IndexError as ie:
                response = f"Invalid command. Try !pzkick USER"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"kickuser", f"{user}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzwhitelist(self, ctx):
        """Whitelist a user"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                user = access_split[1]
            except IndexError as ie:
                response = f"Invalid command. Try !pzwhitelist USER"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"addusertowhitelist", f"{user}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzservermsg(self, ctx):
        """Broadcast a server message"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            try:
                access_split = access_split[1:]
                smsg = " ".join(access_split)
            except IndexError as ie:
                response = f"Invalid command. Try !pzservermsg My cool message"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f'servermsg', f"{smsg}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzunwhitelist(self, ctx):
        """Remove a whitelisted user"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            access_split = ctx.message.content.split()
            user = ""
            try:
                user = access_split[1]
            except IndexError as ie:
                response = f"Invalid command. Try !pzunwhitelist USER"
                await ctx.send(response)
                return
            c_run = await rcon_command(ctx,[f"removeuserfromwhitelist", f"{user}"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzwhitelistall(self, ctx):
        """Whitelist all active users"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            c_run = await rcon_command(ctx,[f"addalltowhitelist"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzsave(self, ctx):
        """Save the current world"""
        await IsChannelAllowed(ctx)
        if await IsAdmin(ctx):
            print(ctx.message.content)
            c_run = await rcon_command(ctx,[f"save"])
            response = f"{c_run}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


bot.add_cog(AdminCommands())


class UserCommands(commands.Cog):
    """Commands open to users"""
    @commands.command(pass_context=True)
    async def pzplayers(self, ctx):
        """Show current active players on the server"""
        await IsChannelAllowed(ctx)
        c_run = ""
        c_run = await rcon_command(ctx, ["players"])
        c_run = "\n".join(c_run.split('\n')[1:-1])
        results = f"Current players in game:\n{c_run}"
        await ctx.send(results)




    @commands.command(pass_context=True)
    async def pzgetoption(self, ctx):
        """Get the value of a server option"""
        await IsChannelAllowed(ctx)
        cmd_split = ctx.message.content.split()
        option_find = ""
        try:
            option_find = cmd_split[1]
        except IndexError as ie:
            response = f"Invalid command. Try !pzgetoption OPTIONNAME"
            await ctx.send(response)
            return
        copt = await rcon_command(ctx,'showoptions')
        copt_split = copt.split('\n')
        match = list(filter(lambda x: option_find.lower() in x.lower(), copt_split))
        match = '\n'.join(list(map(lambda x: x.replace('* ',''),match)))
        results = f"Server options:\n{match}"
        await ctx.send(results)


    @commands.command(pass_context=True)
    async def pzdeathcount(self, ctx):
        """Get the total death count of a player"""
        await IsChannelAllowed(ctx)
        cmd_split = ctx.message.content.split()
        option_find = ""
        try:
            username = cmd_split[1]
        except IndexError as ie:
            response = f"Invalid command. Try !pzdeathcount USERNAME"
            await ctx.send(response)
            return
        dc = await GetDeathCount(ctx, username)
        results = dc
        await ctx.send(results)

bot.add_cog(UserCommands())

async def pzplayers():
    c_run = ""
    c_run = await rcon_command(None, ["players"])
    c_run = "\n".join(c_run.split('\n')[1:-1])
    return len(c_run)

async def status_task():
    while True:
        _serverUp = await IsServerRunning()
        if _serverUp:
            playercount = await pzplayers()
            await bot.change_presence(activity=discord.Game(name=f"{playercount} survivors online"))
        else:
            await bot.change_presence(activity=discord.Game(name=f"Server offline"))
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    bot.loop.create_task(status_task())

print("Starting bot")
bot.run(TOKEN)
