from flask import Flask, render_template, request, jsonify, redirect
import json
import requests

auth_link = "http://127.0.0.1:5005/auth/login"

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def application(): 
    if True:
        return redirect(auth_link)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)