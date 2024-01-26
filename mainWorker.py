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


    def isLoggedIn(self):
        isLoggedIn = self.__databaseManager.isLoggedIn()
        if isLoggedIn:
            discordToken = self.__databaseManager.getLoginToken()
            discordManager.connectIfNecessary(discordToken)  # TODO HERE
            self.waitUntilConnected()
            self.initializeIdsIfNeeded()
            return isLoggedIn, discordToken # make a continue function or something idk
        return isLoggedIn, constants.tokenPlaceholder


    @staticmethod
    async def runServerCreator():
        print("Got run")
        result = await discordManager.createServer()
        return result

    def initializeIdsIfNeeded(self):
        print("HERE")
        loginToken = self.__databaseManager.getLoginToken()
        self.__databaseManager.initializeIdsIfNeeded(loginToken)
        serverId = self.__databaseManager.getServerId()
        print("HERE2")
        if serverId is None:
            print("HERE3")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Use asyncio.run_coroutine_threadsafe to run the async function
            future = asyncio.run_coroutine_threadsafe(self.runServerCreator(), loop)

            # Wait for the result
            result = future.result()

            # self.discord_worker_thread = threading.Thread(target=discordManager.createServer)
            # self.discord_worker_thread.start()
            serverId = self.waitForServerId()


            print("salut, se blocheaza aici?")
            channelId = asyncio.run(discordManager.createChannel(serverId))
            print(f"Server id: {serverId}, channel id: {channelId}")
            self.__databaseManager.setServerId(loginToken, serverId)
            self.__databaseManager.setChannelId(loginToken, channelId)
        else:
            print("HERE132134567890-89876765433253647586565")
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
        discordManager.connectIfNecessary(discordToken)  # TODO HERE
        self.initializeIdsIfNeeded()

