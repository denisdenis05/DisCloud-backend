import json


class DatabaseManager:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__loadFile()

    def isLoggedIn(self):
        return self.__data["loggedIn"]

    def getLoginToken(self):
        if "token" in self.__data["loginData"]:
            return self.__data["loginData"]["token"]
        return None

    def getServerId(self):
        token = self.getLoginToken()
        if "serverId" in self.__data["loginData"][token]:
            return self.__data["loginData"][token]["serverId"]
        return None

    def getChannelId(self):
        token = self.getLoginToken()
        if "channelId" in self.__data["loginData"][token]:
            return self.__data["loginData"][token]["channelId"]
        return None

    def initializeIdsIfNeeded(self, token):
        if token not in self.__data["loginData"]:
            self.__data["loginData"][token] = {}
        self.__save_file()

    def setLoggedInStatus(self, status):
        if type(status) != bool:
            return
        self.__data["loggedIn"] = status
        self.__save_file()

    def setLoginToken(self, token):
        self.__data["loginData"]["token"] = token
        self.__save_file()

    def setServerId(self, loginToken, serverId):
        self.__data["loginData"][loginToken]["serverId"] = serverId
        self.__save_file()

    def setChannelId(self, loginToken, channelId):
        self.__data["loginData"][loginToken]["channelId"] = channelId
        self.__save_file()

    def __loadFile(self):
        try:
            with open(self.__filename, "r+") as fileToRead:
                return json.load(fileToRead)
        except FileNotFoundError:
            baseData = {"loggedIn": False,
                        "loginData": {}}
            return baseData

    def __save_file(self):
        with open(self.__filename, "w+") as fileToWrite:
            json.dump(self.__data, fileToWrite, default=vars)
