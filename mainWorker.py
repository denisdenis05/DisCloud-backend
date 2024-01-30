import asyncio
import threading
from tempfile import TemporaryFile, NamedTemporaryFile

import constants
import discordManager
from database_manager import DatabaseManager



class MainWorker:
    def __init__(self):
        self.__databaseManager = DatabaseManager(constants.jsonFileLocation)
        self.discord_worker_thread = None


    @staticmethod
    def waitUntilConnected():
        while not discordManager.isConnected():
            pass

    def waitForServerId(self):
        while True:
            serverId = self.__databaseManager.getServerId()
            if serverId is not None:
                return serverId

    def waitForChannelId(self):
        while True:
            channelId = self.__databaseManager.getChannelId()
            if channelId is not None:
                return channelId

    @staticmethod
    def checkIfFileIsGoodSize(file):
        return file.tell() / 1024 / 1024 <= constants.maxFileSize


    def getAllStoredFiles(self, loginToken):
        storedFiles = self.__databaseManager.getAllStoredFiles(loginToken)
        return storedFiles

    def isLoggedIn(self):
        isLoggedIn = self.__databaseManager.isLoggedIn()
        if isLoggedIn:
            discordToken = self.__databaseManager.getLoginToken()
            discordManager.connectIfNecessary(discordToken)  # TODO HERE
            self.waitUntilConnected()
            self.initializeIdsIfNeeded()
            return isLoggedIn, discordToken  # make a continue function or something idk
        return isLoggedIn, constants.tokenPlaceholder



    async def runServerCreator(self, loginToken):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.createServer(self.__databaseManager), discordManager.discord_current_running_loop)
        result = result_future.result()
        self.__databaseManager.setServerId(loginToken, result)
        return result

    def runChannelCreator(self, loginToken, serverId):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.createChannel(serverId, self.__databaseManager), discordManager.discord_current_running_loop)
        result = result_future.result()
        self.__databaseManager.setChannelId(loginToken, result)
        return result

    @staticmethod
    def runDeleteMessage(channelId, messageId):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.deleteMessage(channelId, messageId), discordManager.discord_current_running_loop)
        result = result_future.result()
        return result


    @staticmethod
    def runMessageFileSender(channelId, spooledFile):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.sendFileMessage(channelId, spooledFile), discordManager.discord_current_running_loop)
        result = result_future.result()
        return result


    def initializeIdsIfNeeded(self):
        loginToken = self.__databaseManager.getLoginToken()
        self.__databaseManager.initializeIdsIfNeeded(loginToken)
        serverId = self.__databaseManager.getServerId()
        if serverId is None:
            asyncio.run(self.runServerCreator(loginToken))
            serverId = self.waitForServerId()

            asyncio.run(self.runChannelCreator(loginToken, serverId))
            channelId = self.waitForChannelId()
        else:
            channelId = self.__databaseManager.getChannelId()
            if channelId is None:
                asyncio.run(self.runChannelCreator(loginToken, serverId))
                channelId = self.waitForChannelId()


    def uploadFile(self, spooledFile):
        spooledFile.seek(0)
        if self.checkIfFileIsGoodSize(spooledFile):
            channelId = self.__databaseManager.getChannelId()
            messageId = self.runMessageFileSender(channelId, spooledFile)
            fileSize = round(spooledFile.tell() / 1024 / 1024, 3)
            fileName = spooledFile.filename
            self.__databaseManager.addStoredFile(self.__databaseManager.getLoginToken(), [fileName, fileSize], messageId)
        # TODO else split the file in multiple files and upload them to discord as replies to each message until the file is fully uploaded


    def deleteFile(self, fileId):
        channelId = self.__databaseManager.getChannelId()
        messageId = self.runDeleteMessage(channelId, fileId)
        self.__databaseManager.deleteStoredFile(fileId)


    def logOut(self):
        self.__databaseManager.setLoggedInStatus(False)
        self.__databaseManager.setLoginToken(constants.tokenPlaceholder)

    def logIn(self, discordToken):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(discordToken)
        discordManager.connectIfNecessary(discordToken)
        self.initializeIdsIfNeeded()

