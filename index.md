# Project Zomboid Discord Bot
Discord bot for managing your PZ server and enabling player interactions

![spiffo](/project_zomboid_bot/docs/assets/images/Spiffoskip.png)

# Features
#### Bot status displays the server status. Either offline, or player count ingame:
Bot updates it's status with either the current count of players ingame  
or 'Offline' if the server is currently down  
![zombot](/project_zomboid_bot/docs/assets/images/zombot.PNG)

Join and leave announcements  
![zombot](/project_zomboid_bot/docs/assets/images/joined.png)

#### Role based commands
Limit administrative server commands to users with specific discord roles  
![permissions](/project_zomboid_bot/docs/assets/images/permissions.png)  

Moderators can do everything except elevate to admin

Give players insight into their time on the server, like death counts (more to come here):  
![deathcount](/project_zomboid_bot/docs/assets/images/deathcount.PNG)  


#### User Self Service
Players with the correct role can request access to the server whitelist via a command  
The bot will DM them with their new password and connection information to the server  
![access](/project_zomboid_bot/docs/assets/images/access.png)  
```
!pzrequestaccess someuser  
```

### This must be locally hosted on your PZ server due to the interactions it requires to get specific information
Due to how this bot interacts with the server for specific information (rcon, log files, active processes) it must be running on the server that runs project zomboid

I will not go into how to setup a bot or a service for a python script here, there are tons of guides already, but have included basic unit files for this bot


pzbot.py - Handles all commands and server communication. It also will handle the bot status changing and updating. 


pzwatcher.py - Will watch logs and report ingame activities to specified channels


You can use one or the other, or both.

# Requirements and Setup
Make sure you have python3-pip

This requires the rcon executable in the same directory as the script  
**Yes, I tried using python rcon, and python-valve but it did not work and consistently timed out talking to the pz server**

https://leviwheatcroft.github.io/selfhosted-awesome-unlist/rcon-cli.html

```pip install rcon python-dotenv discord.py psutil watchgod file_read_backwards```

Make sure your PZ rcon server is listening on 27015

Create a .env file in the same directory as the pzbot.py file  
All of these should be filled out. To get channel id's, enable dev mode on your discord app, and right click a channel and click 'copy id'   
```
RCON_PASS=SuperPassword
RCON_SERVER=127.0.0.1
RCON_PORT=27015
DISCORD_GUILD="My Discord Server"
DISCORD_TOKEN=CoolTokenHere
ADMIN_ROLES="Admin, Moderator"
LOG_PATH="/home/steamd/Zomboid/Logs"
NOTIFICATION_CHANNEL="123123211"
INGAME_CHANNEL="123123123123213"
PROCESS_NAME="ProjectZomboid64"
WHITELIST_ROLES="Survivor"
SERVER_ADDRESS="69.164.202.83:16261"
```
LOG_PATH should point to where the PZ server logs root is. This is how the player deaths are reported.

ADMIN_ROLES are the discord server roles that will allow those users to run 'AdminCommands'

INGAME_CHANNEL is the channel that project zomboid is attached to, and it gets excluded from command runs

NOTIFICATION_CHANNEL will send player death and join/leave notification

WHITELIST_ROLES="Survivor" - The role name of users that can request accounts on the pz server

SERVER_ADDRESS="1.2.3.4:16261"

Start the bot script

Default settings are setup to work with this installer: https://github.com/rfalias/project_zomboid_installer
# Usage
```
AdminCommands:
  pzsetaccess     Set the access level of a specific user.
ModeratorCommands:
  pzgetsteamid    Lookup steamid of user
  pzkick          Kick a user
  pzsave          Save the current world
  pzservermsg     Broadcast a server message
  pzsteamban      Steam ban a user
  pzsteamunban    Steam unban a user
  pzteleport      Teleport a user to another user
  pzunwhitelist   Remove a whitelisted user
  pzwhitelist     Whitelist a user
  pzwhitelistall  Whitelist all active users
UserCommands:
  pzdeathcount    Get the total death count of a player
  pzdeaths        Get the total death count of al players
  pzgetoption     Get the value of a server option
  pzlistmods      List currently installed mods
  pzplayers       Show current active players on the server
  pzrequestaccess Request access to the PZ server. A password will be DMd to ...
​No Category:
  help            Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```

# Examples
Admin commands can only be run by users in discord with the "Admin" role. 

## Ban a user
!pzsteamban SteamIDOfUser

## Make a user an admin
!pzsetaccess SomeUser admin

## Get a server option
Does a fuzzy lookup for a specific server option

!pzgetoption zombie
```
Server options:
ZombieUpdateDelta=0.5
ZombieUpdateMaxHighPriority=50
ZombieUpdateRadiusHighPriority=10.0
ZombieUpdateRadiusLowPriority=45.0
```
