import asyncio

import constants
import discordManager
from database_manager import DatabaseManager


class MainWorker:
    def __init__(self):
        self.__databaseManager = DatabaseManager(constants.jsonFileLocation)

    def isLoggedIn(self):
        isLoggedIn = self.__databaseManager.isLoggedIn()
        if isLoggedIn:
            discordToken = self.__databaseManager.getLoginToken()
            discordManager.connectIfNecessary(discordToken)
            self.initializeIdsIfNeeded()
            return isLoggedIn, discordToken # make a continue function or something idk
        return isLoggedIn, constants.tokenPlaceholder

    def initializeIdsIfNeeded(self):
        loginToken = self.__databaseManager.getLoginToken()
        self.__databaseManager.initializeIdsIfNeeded(loginToken)
        serverId = self.__databaseManager.getServerId()
        if serverId is None:
            serverId = asyncio.run(discordManager.createServer())
            channelId = asyncio.run(discordManager.createChannel(serverId))
            print(f"Server id: {serverId}, channel id: {channelId}")
            self.__databaseManager.setServerId(loginToken, serverId)
            self.__databaseManager.setChannelId(loginToken, channelId)
        else:
            channelId = self.__databaseManager.getChannelId()
            if channelId is None:
                channelId = discordManager.createChannel(serverId)
            self.__databaseManager.setChannelId(loginToken, channelId)

    def logOut(self):
        self.__databaseManager.setLoggedInStatus(False)
        self.__databaseManager.setLoginToken(constants.tokenPlaceholder)

    def logIn(self, discordToken):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(discordToken)
        discordManager.connectIfNecessary(discordToken)
        self.initializeIdsIfNeeded()

