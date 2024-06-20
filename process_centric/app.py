from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def application():    
    return

if __name__ == "__main__":
    app.run(debug=True, port=5000)