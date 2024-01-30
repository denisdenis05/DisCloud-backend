import json


class DatabaseManager:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__loadFile()

    def isLoggedIn(self):
        self.__updateData()
        return self.__data["loggedIn"]

    def getLoginToken(self):
        self.__updateData()
        if "token" in self.__data["loginData"]:
            return self.__data["loginData"]["token"]
        return None

    def getServerId(self):
        self.__updateData()
        token = self.getLoginToken()
        if "serverId" in self.__data["loginData"][token]:
            return self.__data["loginData"][token]["serverId"]
        return None

    def getChannelId(self):
        self.__updateData()
        token = self.getLoginToken()
        if "channelId" in self.__data["loginData"][token]:
            return self.__data["loginData"][token]["channelId"]
        return None

    def getAllStoredFiles(self, loginToken):
        self.__updateData()
        if loginToken in self.__data["loginData"]:
            if "storedFiles" in self.__data["loginData"][loginToken]:
                return self.__data["loginData"][loginToken]["storedFiles"]
        return {}


    def initializeIdsIfNeeded(self, token):
        self.__updateData()
        if token not in self.__data["loginData"]:
            self.__data["loginData"][token] = {}
        self.__save_file()

    def setLoggedInStatus(self, status):
        self.__updateData()
        if type(status) != bool:
            return
        self.__data["loggedIn"] = status
        self.__save_file()

    def addStoredFile(self, loginToken, fileData, messageId):
        self.__updateData()
        if "storedFiles" not in self.__data["loginData"][loginToken]:
            self.__data["loginData"][loginToken]["storedFiles"] = {}
        self.__data["loginData"][loginToken]["storedFiles"][messageId] = fileData
        self.__save_file()

    def setLoginToken(self, token):
        self.__updateData()
        self.__data["loginData"]["token"] = token
        self.__save_file()

    def setServerId(self, loginToken, serverId):
        self.__updateData()
        self.__data["loginData"][loginToken]["serverId"] = serverId
        self.__save_file()

    def setChannelId(self, loginToken, channelId):
        self.__updateData()
        self.__data["loginData"][loginToken]["channelId"] = channelId
        self.__save_file()

    def __updateData(self):
        self.__data = self.__loadFile()


    def deleteStoredFile(self, fileId):
        fileId = str(fileId)
        self.__updateData()
        for token in self.__data["loginData"]:
            if "storedFiles" in self.__data["loginData"][token]:
                if fileId in self.__data["loginData"][token]["storedFiles"]:
                    self.__data["loginData"][token]["storedFiles"].pop(fileId)
                    self.__save_file()
                    return


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
