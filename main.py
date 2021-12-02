from flask import Flask, render_template, request, redirect, jsonify
from cryptography.fernet import Fernet
import os
import pyaes, pbkdf2, binascii, os, secrets



import rsa

app = Flask(__name__)

STUDENT_CHOICES = {}
ELECTIVES = [
    "Smart Technology",
    "Artificial Intelligence",
    "Immersive Technologies",
    "Service Oriented Architecture"
]


@app.route("/")
def index():
    return render_template("index.html", electives=ELECTIVES)


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    print(email)
    elective = request.form.get("elective")
    if not email or not elective or elective not in ELECTIVES:
        return render_template("failure.html")
    # STUDENTS_CHOICES[email]=elective
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO students(name, elective) VALUES (%s, %s)", (email, elective))
    # mysql.connection.commit()
    # cur.close()

    return redirect("/registrants")


@app.route("/login", methods=['GET', 'POST'])
def login():
    email = "pgarfield@gmail.com"
    password = "password"
    content = request.json
    # must add in encryption and decryption in future
    if content['email'] == email and content['password'] == password:
        result = {"Result": "True",
                  "HouseID": "1234567"
                  }
        return result
    else:
        return "False"


# returns the house main room details
@app.route("/house_room/<house_id>", methods=['GET', 'POST'])
# returns the rooms that the house has
def home_rooms(house_id):
    key= "7625e224dc0f0ec91ad28c1ee67b1eb96d1a5459533c5c950f44aae1e32f2da3"
    iv = "101315118313650930995547809318182348577749662182204730410557592337503452909597"
    test= "sfsdfd";
    print(key)
    print(iv)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    print(aes)
    ciphertext = aes.encrypt(test)
    print('Encrypted:', binascii.hexlify(ciphertext))
    rooms = [{
        "temperature": 10,
        "dateTime": "24:00:15T2021:12:02",
        "room": "Bedroom #1"
    },
        {
            "temperature": 20,
            "dateTime": "24:00:15T2021:12:02",
            "room": "Kitchen #2"
        }]
    if house_id == "1234567":
        return jsonify(rooms)
    else:
        return str(house_id)


@app.route("/oil_level_current/<house_id>", methods=['GET', 'POST'])
# returns the rooms that the house has
def current_levels(house_id):
    # get the most recent recording of the oil
    result = {
        "oil_level": 10,  # percent out a hundred in number
    }
    if house_id == "1234567":
        return jsonify(result)
    else:
        return str(house_id)


# needed for home page
@app.route("/average_temperature_house/<house_id>", methods=['GET'])
def average_temperature(house_id):
    # get the average temperature of the house
    result = {
        "temperature": 30,  # return as int
    }
    if house_id == "1234567":
        return jsonify(result)
    else:
        return str(house_id)


app.run(debug=True)


# get oil usage last 7 days
@app.route("/usage/<house_id>", methods=['GET'])
def usage_last_7(house_id):
    # get the usage last 7 days
    result = [{
        "oilUsed": 100,  # oil used in litres
        "day": "2021:11:02",
    },
        {
            "oilUsed": 7000,  # oil used in litres
            "day": "2021:11:03",
        },
        {
            "oilUsed": 0,  # oil used in litres
            "day": "2021:11:04",
        },
        {
            "oilUsed": 50,  # oil used in litres
            "day": "2021:11:05",
        },
        {
            "oilUsed": 1000,  # oil used in litres
            "day": "2021:11:06",
        },
        {
            "oilUsed": 1000,  # oil used in litres
            "day": "2021:11:07",
        },
        {
            "oilUsed": 1000,  # oil used in litres
            "day": "2021:11:086",
        }]
    if house_id == "1234567":
        return jsonify(result)
    else:
        return str(house_id)





app.run(debug=True)
