import json


class DatabaseManager:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__loadFile()

    def isLoggedIn(self):
        return self.__data["loggedIn"]

    def getLoginToken(self):
        return self.__data["loginData"]["token"]

    def setLoggedInStatus(self, status):
        if type(status) != bool:
            return
        self.__data["loggedIn"] = status
        self.__save_file()

    def setLoginToken(self, token):
        self.__data["loginData"]["token"] = token
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
