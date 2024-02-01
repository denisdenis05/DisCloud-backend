import asyncio
import threading
from tempfile import TemporaryFile, NamedTemporaryFile, SpooledTemporaryFile

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


    def checkIfFileIsGoodSize(self, file):
        fileSize = self.getFileSizeInMB(file)
        return fileSize <= constants.maxFileSize

    @staticmethod
    def getFileSizeInMB(file):
        file.seek(0, 2)
        return file.tell() / 1024 / 1024


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
            return isLoggedIn, discordToken
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
    def runDownloadFile(channelId, messageId):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.downloadFile(channelId, messageId), discordManager.discord_current_running_loop)
        result = result_future.result()
        return result

    @staticmethod
    def runMessageFileSender(channelId, spooledFile, latestMessageId=None):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.sendFileMessage(channelId, spooledFile, latestMessageId), discordManager.discord_current_running_loop)
        result = result_future.result()
        return result

    @staticmethod
    def runCheckIfMessageIsReply(channelId, messageId):
        result_future = asyncio.run_coroutine_threadsafe(discordManager.CheckIfMessageIsReply(channelId, messageId), discordManager.discord_current_running_loop)
        result = result_future.result()
        return result


    def manageMultipleUploadFiles(self, channelId, resultedFiles):
        latestMessageId = None
        for file in resultedFiles:
            file.seek(0)
            messageId = self.runMessageFileSender(channelId, file, latestMessageId)
            latestMessageId = messageId
        return latestMessageId


    """
    SOMETHING SOMETHING
    """


    @staticmethod
    def splitFileInMultiple24MBFiles(spooledFile):
        resultedFiles = []

        spooledFile.seek(0)
        fileContent = spooledFile.read()

        chunkSize = 24 * 1024 * 1024
        numChunks = (len(fileContent) + chunkSize - 1) // chunkSize

        for indexOfChunk in range(numChunks):
            start = indexOfChunk * chunkSize
            end = (indexOfChunk + 1) * chunkSize

            chunkData = fileContent[start:end]

            chunkSpooledFile = SpooledTemporaryFile(mode='wb')
            chunkSpooledFile.write(chunkData)
            resultedFiles.append(chunkSpooledFile)
        return resultedFiles







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
            spooledFile.seek(0)
            channelId = self.__databaseManager.getChannelId()
            messageId = self.runMessageFileSender(channelId, spooledFile)

            fileSize = round(self.getFileSizeInMB(spooledFile), 3)
            fileName = spooledFile.filename
            spooledFile.seek(0)

            self.__databaseManager.addStoredFile(self.__databaseManager.getLoginToken(), [fileName, fileSize], messageId)
        else:
            fileSize = round(self.getFileSizeInMB(spooledFile), 3)
            fileName = spooledFile.filename
            spooledFile.seek(0)

            resultedFiles = self.splitFileInMultiple24MBFiles(spooledFile)
            channelId = self.__databaseManager.getChannelId()
            messageId = self.manageMultipleUploadFiles(channelId, resultedFiles)

            self.__databaseManager.addStoredFile(self.__databaseManager.getLoginToken(), [fileName, fileSize], messageId)

    def deleteFile(self, fileId):
        channelId = self.__databaseManager.getChannelId()
        messageId = self.runDeleteMessage(channelId, fileId)
        self.__databaseManager.deleteStoredFile(fileId)

    def downloadFile(self, fileId):
        loginToken = self.__databaseManager.getLoginToken()
        channelId = self.__databaseManager.getChannelId()
        downloadName = self.__databaseManager.getDownloadName(loginToken, fileId)
        messageIsReply = True

        downloadedFiles = []

        while messageIsReply:
            currentFile = self.runDownloadFile(channelId, fileId)
            downloadedFiles.append(currentFile)
            checkIfMessageIsReply = self.runCheckIfMessageIsReply(self.__databaseManager.getChannelId(), fileId)
            if checkIfMessageIsReply is None:
                messageIsReply = False
            else:
                fileId = checkIfMessageIsReply

        if len(downloadedFiles) == 1:
            return downloadedFiles[0], downloadName
        else:
            finalFile = SpooledTemporaryFile(mode='wb')
            for downloadedFile in reversed(downloadedFiles):
                finalFile.write(downloadedFile)
            finalFile.seek(0, 2)
        finalFile.seek(0)
        fileData = finalFile.read()
        return fileData, downloadName

    def logOut(self):
        self.__databaseManager.setLoggedInStatus(False)
        self.__databaseManager.setLoginToken(constants.tokenPlaceholder)

    def logIn(self, discordToken):
        self.__databaseManager.setLoggedInStatus(True)
        self.__databaseManager.setLoginToken(discordToken)
        discordManager.connectIfNecessary(discordToken)
        self.initializeIdsIfNeeded()

