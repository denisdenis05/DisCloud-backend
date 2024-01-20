import asyncio

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", help_command=None, intents=intents, case_insensitive=True)



@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')


def connectIfNecessary(botToken):
    if client.is_closed():
        asyncio.run(client.close())
        runTheBot(botToken)

def runTheBot(botToken):
    asyncio.run(client.run(botToken))

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
    serverName = "ServerToUploadThingsTo"
    try:
        server = await client.create_guild(name=serverName)
        print(f"Guild '{server.name}' created with ID {server.id}")
        return server.id
    except discord.HTTPException as e:
        print(f"Error creating guild: {e}")
