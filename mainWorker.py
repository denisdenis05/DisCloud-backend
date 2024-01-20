import constants
from database_manager import DatabaseManager


class MainWorker:
    def __init__(self):
        self.__databaseManager = DatabaseManager(constants.jsonFileLocation)

    def isLoggedIn(self):
        isLoggedIn = self.__databaseManager.isLoggedIn()
        if isLoggedIn:
            discordToken = self.__databaseManager.getLoginToken()
            return isLoggedIn, discordToken
        return isLoggedIn, constants.tokenPlaceholder

    def logOut(self):
        self.__databaseManager.setLoggedInStatus(False)
        self.__databaseManager.setLoginToken(constants.tokenPlaceholder)

    def logIn(self, token):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(token)

