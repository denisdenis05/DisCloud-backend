from flask import Flask, jsonify, request
from flask_cors import CORS

mainApp = Flask(__name__)
CORS(mainApp)

@mainApp.route('/api/test', methods=['GET'])
def test():
    data = {"test": "test2"}
    return jsonify(data)


mainApp.run(port=5000)


