import asyncio
import threading

import discord
from discord.ext import commands, tasks

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", help_command=None, intents=intents, case_insensitive=True)
discord_thread = None
discord_current_running_loop = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    global discord_current_running_loop
    discord_current_running_loop = asyncio.get_running_loop()
    for guild in client.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

    return


def connectIfNecessary(botToken):
    global discord_thread
    global client
    if discord_thread is None or client.user is None or client.is_closed():
        discord_thread = threading.Thread(target=runTheBot, args=(botToken,))
        discord_thread.start()

def runTheBot(botToken):
    client.run(botToken)

async def createChannel(serverId, databaseManager):
    guild = client.get_guild(serverId)
    if guild:
        channelName = "ChannelToUploadThingsTo"
        channel = await guild.create_text_channel(channelName)
        return channel.id
    else:
        print(f"Guild with ID {serverId} not found")

async def createServer(databaseManager):
    global client
    serverName = "ServerToUploadThingsTo"
    try:
        server = await client.create_guild(name=serverName)
        return server.id
    except discord.HTTPException as e:
        print(f"Error creating guild: {e}")

def isConnected():
    global client
    return client.is_ready()