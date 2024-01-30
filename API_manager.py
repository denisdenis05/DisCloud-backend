from flask import Flask, jsonify, request
from flask_cors import CORS
from mainWorker import MainWorker

mainApp = Flask(__name__)
CORS(mainApp)
mainWorker = MainWorker()



@mainApp.route('/api/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        data = {"test": "test2"}
        return jsonify(data)
    elif request.method == 'POST':
        requestData = request.get_json()
        resultData = {"receivedData": requestData}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/api/checkIfLoggedIn', methods=['GET'])
def checkIfLoggedIn():
    if request.method == 'GET':
        isLoggedIn, discordToken = mainWorker.isLoggedIn()
        if isLoggedIn:
            storedFiles = mainWorker.getAllStoredFiles(discordToken)
        else:
            storedFiles = {}
        dataToBeSent = {"isLoggedIn": isLoggedIn, "discordToken": discordToken, "storedFiles": storedFiles}
        dataToBeSent = jsonify(dataToBeSent)
        return dataToBeSent
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/api/disconnectFromDiscord', methods=['GET'])
def disconnectFromDiscord():
    if request.method == 'GET':
        mainWorker.logOut()
        dataToBeSent = {}
        return jsonify(dataToBeSent)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/api/connectToDiscord', methods=['POST'])
def connectToDiscord():
    if request.method == 'POST':
        requestData = request.get_json()
        mainWorker.logIn(requestData["token"])
        dataToBeSent = {}
        return jsonify(dataToBeSent)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        discordId = request.get_json()
        resultData = {"receivedId": discordId}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405


@mainApp.route('/api/deleteFile', methods=['POST'])
def deleteFile():
    if request.method == 'POST':
        requestData = request.get_json()
        print(requestData)
        mainWorker.deleteFile(int(requestData["fileId"]))
        dataToBeSent = {}
        return jsonify(dataToBeSent)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/api/uploadFile', methods=['POST'])
def uploadFile():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        else:
            spooledFile = request.files['file']
            if spooledFile.filename == '':
                return jsonify({"error": "No selected file"}), 400
            mainWorker.uploadFile(spooledFile)

            resultData = {"receivedId": spooledFile.filename}
            return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405


exportedMainApp = mainApp
