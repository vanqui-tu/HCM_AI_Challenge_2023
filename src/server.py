from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import json
import csv

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your Flask app

app.static_url_path = '/static'  # This sets the URL path for the static files
app.static_folder = '../data/keyframes' 

print("### | Initial model...")
from aic23_model import model

print("### | Get detail keyframes...")
with open("../data/detail_keyframes.json", "r") as json_file:
    detail_keyframes = json.load(json_file)

print("### | Get all objects...")
objects = []
with open(f"../data/object_labels.csv", 'r', newline="") as file:
    csv_reader = csv.reader(file)
    next(csv_reader, None)

    for row in csv_reader:
        objects.append(row)

@app.route('/initial', methods=['GET'])
def initial():
    try:
        # Your processing logic goes here
        # For demonstration purposes, let's just echo the received data
        result = {"message": "successful", "detail_keyframes": detail_keyframes[:100], "objects": objects}

        # Return a JSON response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/search', methods=['POST'])
def search():
    try:
        # Get the JSON data from the client's request
        data = request.json
        query = data["searchQuery"]
        results = model.search(
            query_text=query,
            audio_texts=[],
            topk=200,
        ) 

        print(results.to_json())

        # Your processing logic goes here
        # For demonstration purposes, let's just echo the received data
        result = {"message": "Received data successfully", "data": results.to_json()}

        # Return a JSON response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("<<<<<< SERVER RUN | http://localhost:5000 >>>>>>")
    app.run(debug=True, port=5000)
