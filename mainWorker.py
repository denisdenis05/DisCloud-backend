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
            return isLoggedIn, discordToken
        return isLoggedIn, constants.tokenPlaceholder

    def runTheBotAsFirstTime(self):
        loginToken = self.__databaseManager.getLoginToken()
        discordManager.connectIfNecessary(loginToken)
        serverId = self.__databaseManager.getServerId()
        if serverId is None:
            serverId = discordManager.createServer()
            channelId = discordManager.createChannel(serverId)
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

    def logIn(self, token):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(token)
        self.runTheBotAsFirstTime()

