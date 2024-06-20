from flask import Flask, request, redirect, jsonify
import requests
import json
import psycopg2
from dotenv import load_dotenv
import os
from consts import DATA_URL

app = Flask(__name__)




@app.route("/gear", methods = ["POST"])
def suggest_gear():
    data = request.json
    length = data["length"]
    elevations = data["elevations"]
    min_elevation = min(elevations)
    max_elevation = max(elevations)
    temp = data["temperature"]
    weather = data["weather"]
    prec = data["prec"]
    gender = data["gender"]
    parameters = calculate_gear_parameters(length, max_elevation, min_elevation, temp, weather, prec)
    gear_response = requests.post(DATA_URL, json = {
        "warmth": parameters[0], 
        "waterproof": parameters[1], 
        "level": parameters[2],
        "gender": gender,
    })
    gear = gear_response.json()
    return jsonify(gear)

    
def calculate_gear_parameters(length, max_elevation, min_elevation, temp, weather, prec):
    waterproof = 0

    elevation_gain = max_elevation - min_elevation

    if temp < 5:
        warmth = "high"

    elif temp >= 5 and temp < 20:
        warmth = "medium"
    elif temp >= 20:
        warmth = "low"

    if max_elevation > 2000 and warmth == "low": 
        warmth = "medium"

    if weather["main"] == "Snow":
        warmth = "high"
        waterproof = 10000

    if weather["main"] == "Rain":
        if prec >= 3:
            waterproof = 20000
        elif prec >= 1:
            waterproof = 10000
        else:
            waterproof = 5000
    
    level1 = 0
    level2 = 0
    level3 = 0

    if length >= 6000 and length < 10000:
        level1 = 1
    else:
        level1 = 2

    if elevation_gain >= 300 and elevation_gain < 700:
        level2 = 1
    else:
        level2 = 2

    if max_elevation >= 2000 and max_elevation < 2400:
        level3 = 1
    else:
        level3 = 2

    level_tot = level1 + level2 + level3

    if level_tot <= 2:
        level = "beginner"
    elif level_tot <= 4:
        level = "intermediate"
    else:
        level = "advanced"

    return [warmth, waterproof, level]


if __name__ == "__main__":
    app.run(debug=True, port=5004)