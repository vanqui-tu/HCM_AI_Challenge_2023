from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import json

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your Flask app

with open("../../data/detail_keyframes.json", "r") as json_file:
    detail_keyframes = json.load(json_file)

@app.route('/example', methods=['GET'])
def example():
    try:
        # Your processing logic goes here
        # For demonstration purposes, let's just echo the received data
        result = {"message": "successful", "data": detail_keyframes[:7]}

        # Return a JSON response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/search', methods=['POST'])
def search():
    try:
        # Get the JSON data from the client's request
        data = request.json
        print("Message: ",data)

        # Your processing logic goes here
        # For demonstration purposes, let's just echo the received data
        result = {"message": "Received data successfully", "data": data}

        # Return a JSON response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
