import asyncio
import threading

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", help_command=None, intents=intents, case_insensitive=True)
discord_thread = None


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    return


def connectIfNecessary(botToken):
    global discord_thread
    global client
    if discord_thread is None or client.user is None or client.is_closed():
        discord_thread = threading.Thread(target=runTheBot, args=(botToken,))
        discord_thread.start()

def runTheBot(botToken):
    client.run(botToken)

async def createChannel(serverId):
    guild = client.get_guild(serverId)
    if guild:
        channelName = "ChannelToUploadThingsTo"
        channel = await guild.create_text_channel(channelName)
        print(f"Channel {channel.name} with ID {channel.id} created in {guild.name}")
        return channel.id
    else:
        print(f"Guild with ID {serverId} not found")

async def createServer():
    global client
    serverName = "ServerToUploadThingsTo"
    print("Creating server: |||||| SE BLOCHEAZA AICI???")
    try:
        print("Creating server: |||||| SE BLOCHEAZA AICI 2???")
        server = await client.create_guild(name=serverName)
        print("Creating server: |||||| SE BLOCHEAZA AICI 3???")
        print(f"Guild '{server.name}' created with ID {server.id}")
        return server.id
    except discord.HTTPException as e:
        print(f"Error creating guild: {e}")

def isConnected():
    global client
    return client.is_ready()