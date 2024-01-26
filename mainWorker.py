import asyncio
import threading

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


    def isLoggedIn(self):
        isLoggedIn = self.__databaseManager.isLoggedIn()
        if isLoggedIn:
            discordToken = self.__databaseManager.getLoginToken()
            discordManager.connectIfNecessary(discordToken)  # TODO HERE
            self.waitUntilConnected()
            self.initializeIdsIfNeeded()
            return isLoggedIn, discordToken # make a continue function or something idk
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

    def logOut(self):
        self.__databaseManager.setLoggedInStatus(False)
        self.__databaseManager.setLoginToken(constants.tokenPlaceholder)

    def logIn(self, discordToken):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(discordToken)
        discordManager.connectIfNecessary(discordToken)  # TODO HERE
        self.initializeIdsIfNeeded()

