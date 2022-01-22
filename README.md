# project_zomboid_bot
Discord bot for managing your PZ server. 

I will not go into how to setup a bot or a service for a python script here, there are tons of guides already

# Requirements and Setup
Make sure you have python3-pip

This requires the rcon executable in the same directory as the script

https://leviwheatcroft.github.io/selfhosted-awesome-unlist/rcon-cli.html

```pip install rcon python-dotenv discord.py```

Make sure your PZ rcon server is listening on 27015

Create a .env file in the same directory as the pzbot.py file
```
RCON_PASS=SuperPassword
RCON_SERVER=127.0.0.1
RCON_PORT=27015
DISCORD_GUILD="My Discord Server"
DISCORD_TOKEN=CoolTokenHere
ADMIN_ROLES="Admin, Moderator"
LOG_PATH="/home/steamd/Zomboid/Logs"
```
LOG_PATH should point to where the PZ server logs root is. This is how the player deaths are reported.
ADMIN_ROLES are the discord server roles that will allow those users to run 'AdminCommands'

Start the bot script

# Usage
```
AdminCommands:
  pzkick         Kick a user
  pzsave         Save the current world
  pzservermsg    Broadcast a server message
  pzsetaccess    Set the access level of a specific user.
  pzsteamban     Steam ban a user
  pzsteamunban   Steam unban a user
  pzteleport     Teleport a user to another user
  pzunwhitelist  Remove a whitelisted user
  pzwhitelist    Whitelist a user
  pzwhitelistall Whitelist all active users
UserCommands:
  pzdeathcount   Get the total death count of a player
  pzgetoption    Get the value of a server option
  pzplayers      Show current active players on the server
​No Category:
  help           Shows this message

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
!pzgetoption zombie
```
Server options:
ZombieUpdateDelta=0.5
ZombieUpdateMaxHighPriority=50
ZombieUpdateRadiusHighPriority=10.0
ZombieUpdateRadiusLowPriority=45.0
```
