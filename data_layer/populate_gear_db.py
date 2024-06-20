import psycopg2
from dotenv import load_dotenv
import os
import json

CREATE_GEAR_TABLE = (
    "CREATE TABLE IF NOT EXISTS gear (code INTEGER PRIMARY KEY, description TEXT, gender TEXT, bodypart TEXT, category TEXT, warmth TEXT, waterproof INTEGER, level TEXT, link TEXT);"
)

INSERT_GEAR = "INSERT INTO gear (code, description, gender, bodypart, category, warmth, waterproof, level, link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

DELETE_GEAR_TABLE = "DROP TABLE gear;"




load_dotenv()

url = os.getenv("DATABASE_URL")

connection = psycopg2.connect(url)
    
def populate_gear_table():

    with open('gear_data.json') as gear_json:
        gear_data = json.load(gear_json)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_GEAR_TABLE)
            for gear_element in gear_data:

                code = gear_element["id"]
                description = gear_element["description"]
                gender = gear_element["gender"]
                bodypart = gear_element["body part"]
                category = gear_element["category"]
                warmth = gear_element["warmth"]
                waterproof = gear_element["waterproof"]
                level = gear_element["level"]
                link = gear_element["link"]

                cursor.execute(INSERT_GEAR, (code, description, gender, bodypart, category, warmth, waterproof, level, link))
    return

def delete_gear_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_GEAR_TABLE)  
    return      


delete_gear_table()
populate_gear_table()