import asyncio
import tempfile
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

async def sendFileMessage(channelId, spooledFile, previousMessageId=None):
    global client
    channel = client.get_channel(channelId)
    if channel:
        with tempfile.NamedTemporaryFile(delete=False) as tempFile:
            tempFile.write(spooledFile.read())
            tempFile.seek(0)
            if previousMessageId is None:
                newMessage = await channel.send(file=discord.File(tempFile.name, filename="file"))
            else:
                message = await channel.fetch_message(previousMessageId)
                newMessage = await message.reply(file=discord.File(tempFile.name, filename="file"))
        return newMessage.id
    else:
        print(f"Channel with ID {channelId} not found")


async def CheckIfMessageIsReply(channelId, messageId):
    global client
    channel = client.get_channel(channelId)
    if channel:
        message = await channel.fetch_message(messageId)
        if message.reference:
            return message.reference.message_id
        return None
    else:
        print(f"Channel with ID {channelId} not found")


async def deleteMessage(channelId, messageId):
    global client
    channel = client.get_channel(channelId)
    if channel:
        message = await channel.fetch_message(messageId)
        await message.delete()
    else:
        print(f"Channel with ID {channelId} not found")

async def downloadFile(channelId, messageId):
    global client
    channel = client.get_channel(channelId)
    if channel:
        message = await channel.fetch_message(messageId)
        attachment = message.attachments[0]
        file_content = await attachment.read()
        return file_content
    else:
        print(f"Channel with ID {channelId} not found")


def isConnected():
    global client
    return client.is_ready()