from flask import Flask, request, jsonify
import requests
import json
import logging

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
    gender = data['gender']
    
    [warmth, waterproof, level] = calculate_gear_parameters(length, max_elevation, min_elevation, temp, weather, prec)

    print(warmth, waterproof, level)


    fleece = None
    tshirt = None
    jacket = None
    pants = None
    boots = None
    socks = None
    backpack = None


    # FLEECE
    if warmth != 'low':
        if warmth == 'medium' and level != 'advanced':
            print("Fleece 1")
            fleece = requests.post(DATA_URL, json={
                "warmth": warmth, 
                "category": "fleece", 
                "level": level,
                "waterproof": 'any',
                "gender": gender,
            })
        elif warmth == 'medium' and level == 'advanced':
            print('Fleece 2')
            fleece = requests.post(DATA_URL, json={
                "warmth": warmth, 
                "category": "fleece", 
                "level": 'intermediate',
                "waterproof": 'any',
                "gender": gender,
            })
        elif warmth == 'high':
            print("Fleece 3")
            fleece = requests.post(DATA_URL, json={
                "warmth": warmth, 
                "category": "fleece", 
                "level": 'any',
                "waterproof": 'any',
                "gender": gender,
            })

    # T-SHIRT
    if warmth == 'low' or warmth == 'medium':
        print('t-shirt')
        tshirt = requests.post(DATA_URL, json={ 
                "category": "t-shirt", 
                "warmth": 'any',
                "level": level,
                "waterproof": 'any',
                "gender": gender,
            })


    # JACKET
    if warmth == 'low' and waterproof != 0:
        print('Jacket 1')
        if waterproof <= 5000:
            jacket = requests.post(DATA_URL, json={ 
                "category": "jacket", 
                "warmth": warmth,
                "level": level,
                "waterproof": waterproof,
                "gender": gender,
            })
        else:
            jacket = requests.post(DATA_URL, json={ 
                    "category": "jacket", 
                    "warmth": warmth,
                    "level": 'any',
                    "waterproof": waterproof,
                    "gender": gender,
                })

    elif warmth == 'high' and level == 'beginner':
        print('Jacket 2')
        jacket = requests.post(DATA_URL, json={ 
                "category": "jacket",
                "warmth": warmth, 
                "level": 'any',
                "waterproof": waterproof,
                "gender": gender,
            })
        
    elif warmth == 'high':
        print('Jacket 3')
        jacket = requests.post(DATA_URL, json={ 
                "category": "jacket", 
                "warmth": warmth,
                "level": level,
                "waterproof": waterproof,
                "gender": gender,
            })

    # PANTS
    if warmth == 'low' and level != 'advanced':
        print('Pants 1')
        pants = requests.post(DATA_URL, json={ 
                "category": "shorts", 
                "warmth": warmth,
                "level": level,
                "waterproof": 'any',
                "gender": gender,
            })
    elif warmth == 'low' and level == 'advanced':
        print('Pants 2')
        pants = requests.post(DATA_URL, json={ 
                "category": "shorts", 
                "warmth": warmth,
                "level": 'intermediate',
                "waterproof": 'any',
                "gender": gender,
            })

    elif warmth == 'medium' and level != 'advanced':
        print('Pants 3')
        pants = requests.post(DATA_URL, json={ 
                "category": "pants", 
                "warmth": warmth,
                "level": level,
                "waterproof": 'any',
                "gender": gender,
            })
    elif warmth == 'medium' and level == 'advanced':
        print('Pants 4')
        pants = requests.post(DATA_URL, json={ 
                "category": "pants", 
                "warmth": warmth,
                "level": 'intermediate',
                "waterproof": 'any',
                "gender": gender,
            })
        
    elif warmth == 'high':
        print('Pants 5')
        pants = requests.post(DATA_URL, json={ 
                "category": "pants", 
                "warmth": warmth,
                "level": 'any',
                "waterproof": 'any',
                "gender": gender,
            })
    
    # BOOTS
    boots = requests.post(DATA_URL, json={ 
                "category": "hiking boots",
                "warmth": 'any', 
                "level": level,
                "waterproof": 'any',
                "gender": gender,
            })
    
    # SOCKS
    socks = requests.post(DATA_URL, json={ 
                "category": "hiking socks",
                "warmth": 'any', 
                "level": level,
                "waterproof": 'any',
                "gender": 'any',
            })

    # BACKPACK
    backpack = requests.post(DATA_URL, json={ 
                "category": "backpack",
                "warmth": 'any', 
                "level": level,
                "waterproof": 'any',
                "gender": 'any',
            })

    print(fleece)
    
    if fleece != None:
        if fleece.status_code == 200:
                fleece = fleece.json() if fleece else {}
        else:
            error_message = fleece.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        fleece = {}
    if tshirt != None:
        if tshirt != None and tshirt.status_code == 200:
            tshirt = tshirt.json() if tshirt else {}
        else:
            error_message = tshirt.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        tshirt = {}
    if jacket != None:
        if jacket != None and jacket.status_code == 200:
            jacket = jacket.json() if jacket else {}
        else:
            error_message = jacket.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        jacket = {}
    if pants != None:
        if pants.status_code == 200:
            pants = pants.json() if pants else {}
        else:
            error_message = pants.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        pants = {}
    if boots != None:
        if boots.status_code == 200:
            boots = boots.json() if boots else {}
        else:
            error_message = boots.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        boots = {}
    if socks != None:
        if socks.status_code == 200:
            socks = socks.json() if socks else {}
        else:
            error_message = socks.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        socks = {}
    if backpack != None:
        if backpack.status_code == 200:
            backpack = backpack.json() if backpack else {}
        else:
            error_message = backpack.get('error_message', 'Unknown error')
            return jsonify({"error": error_message}), 400
    else:
        backpack = {}
    gear = {
        'fleece': fleece,
        't-shirt': tshirt,
        'jacket': jacket,
        'pants': pants,
        'boots': boots,
        'socks': socks,
        'backpack': backpack
    }
    

    
    return jsonify(gear)

    
def calculate_gear_parameters(length, max_elevation, min_elevation, temp, weather, prec):
    waterproof = 0

    elevation_gain = max_elevation - min_elevation

    if temp < 2:
        warmth = "high"

    elif temp >= 2 and temp < 25:
        warmth = "medium"
    elif temp >= 25:
        warmth = "low"

    if max_elevation > 2000 and warmth == "low": 
        warmth = "medium"

    if weather == "Snow":
        warmth = "high"
        waterproof = 10000

    if weather == "Rain":
        if prec >= 3:
            waterproof = 20000
        elif prec >= 1:
            waterproof = 10000
        else:
            waterproof = 5000
    print(waterproof)
    level1 = 0
    level2 = 0
    level3 = 0

    if length >= 6000 and length < 15000:
        level1 = 1
    elif length >= 15000:
        level1 = 2

    if elevation_gain >= 300 and elevation_gain < 700:
        level2 = 1
    elif elevation_gain >= 700:
        level2 = 2

    if max_elevation >= 2000 and max_elevation < 2400:
        level3 = 1
    elif max_elevation >= 2400:
        level3 = 2

    print(level1, level2, level3)

    level_tot = level1 + level2 + level3

    if level_tot <= 2:
        level = "beginner"
    elif level_tot <= 3:
        level = "intermediate"
    else:
        level = "advanced"

    return [warmth, waterproof, level]


if __name__ == "__main__":
    app.run(debug=True, port=5004)