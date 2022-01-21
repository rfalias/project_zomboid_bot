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
import asyncio
from concurrent.futures import ThreadPoolExecutor
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rcon import rcon
from rcon import Client

# Setup environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
RCONPASS = os.getenv('RCON_PASS')
RCONSERVER = os.getenv('RCON_SERVER')
RCONPORT = os.getenv('RCON_PORT')
GUILD = os.getenv('DISCORD_GUILD')
ADMIN_ROLES = os.getenv('ADMIN_ROLES')
ADMIN_ROLES = ADMIN_ROLES.split(',')
bot = commands.Bot(command_prefix='!')
access_levels = ['admin', 'none', 'moderator']
intents = discord.Intents.default()
intents.members = True

async def IsAdmin(ctx):
    is_present = [i for i in ctx.author.roles if i.name in ADMIN_ROLES]
    return is_present

class AdminCommands(commands.Cog):
    """Admin Server Commands"""
    @commands.command(pass_context=True)
    async def pzsetaccess(self, ctx): 
        """Set the access level of a specific user."""
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
            c_run = await rcon(f"setaccesslevel {user} {access_level}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Set access of user {user} to {access_level}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzsteamban(self, ctx):
        """Steam ban a user"""
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
            c_run = await rcon(f"banid {user}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Steam banned {user}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzsteamunban(self, ctx):
        """Steam unban a user"""
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
            c_run = await rcon(f"unbanid {user}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Steam unbanned {user}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzkick(self, ctx):
        """Kick a user"""
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
            c_run = await rcon(f"kickuser {user}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Kicked {user}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzwhitelist(self, ctx):
        """Whitelist a user"""
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
            c_run = await rcon(f"addusertowhitelist {user}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Whitelisted {user}"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)

    @commands.command(pass_context=True)
    async def pzunwhitelist(self, ctx):
        """Remove a whitelisted user"""
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
            c_run = await rcon(f"removeuserfromwhitelist {user}", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Removed {user} from whitelist"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzwhitelistall(self, ctx):
        """Whitelist all active users"""
        if await IsAdmin(ctx):
            print(ctx.message.content)
            c_run = await rcon(f"addalltowhitelist", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"Added all current users to the whitelist"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


    @commands.command(pass_context=True)
    async def pzsave(self, ctx):
        """Save the current world"""
        if await IsAdmin(ctx):
            print(ctx.message.content)
            c_run = await rcon(f"save", host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
            response = f"World saved"
        else:
            response = f"{ctx.author}, you don't have admin rights."
        await ctx.send(response)


bot.add_cog(AdminCommands())


class UserCommands(commands.Cog):
    """Commands open to users"""
    @commands.command(pass_context=True)
    async def pzplayers(self, ctx):
        """Show current active players on the server"""
        c_run = await rcon('players', host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
        c_run = "\n".join(c_run.split('\n')[1:-1])
        results = f"Current players in game:\n{c_run}"
        await ctx.send(results)

    @commands.command(pass_context=True)
    async def pzgetoption(self, ctx):
        """Get the value of a server option"""
        cmd_split = ctx.message.content.split()
        option_find = ""
        try:
            option_find = cmd_split[1]
        except IndexError as ie:
            response = f"Invalid command. Try !pzgetoption OPTIONNAME"
            await ctx.send(response)
            return
        copt = await rcon('showoptions', host=RCONSERVER, port=RCONPORT, passwd=RCONPASS)
        copt_split = copt.split('\n')
        match = list(filter(lambda x: option_find.lower() in x.lower(), copt_split))
        match = '\n'.join(list(map(lambda x: x.replace('* ',''),match)))
        results = f"Server options:\n{match}"
        await ctx.send(results)
bot.add_cog(UserCommands())

bot.run(TOKEN)
