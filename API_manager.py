from flask import Flask, jsonify, request
from flask_cors import CORS

mainApp = Flask(__name__)
CORS(mainApp)



@mainApp.route('/api/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        data = {"test": "test2"}
        return jsonify(data)
    elif request.method == 'POST':
        requestData = request.get_json()
        print(requestData)
        resultData = {"receivedData": requestData}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/api/checkIfLoggedIn', methods=['GET'])
def checkIfLoggedIn():
    if request.method == 'GET':
        dataToBeSent = {"isLoggedIn": True, "discordToken": "kdhcscbh"}
        return jsonify(dataToBeSent)
    else:
        return jsonify({"message": "Method not allowed"}), 405

@mainApp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        discordId = request.get_json()
        print(discordId)
        resultData = {"receivedId": discordId}
        return jsonify(resultData)
    else:
        return jsonify({"message": "Method not allowed"}), 405

exportedMainApp = mainApp