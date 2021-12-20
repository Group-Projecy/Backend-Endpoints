import json

from Cryptodome import Random
from Cryptodome.Cipher import AES
from flask import Flask, render_template, request, redirect, jsonify
import secrets
import base64
import base64
from hashlib import md5
app = Flask(__name__)

STUDENT_CHOICES = {}
ELECTIVES = [
    "Smart Technology",
    "Artificial Intelligence",
    "Immersive Technologies",
    "Service Oriented Architecture"
]


#add this------------------------------------------------------------------------------------------------------
BLOCK_SIZE = 16

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length) * length).encode()


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))


password = "YourSecretKeyForEncryption&Descryption".encode()
ct_b64 = "U2FsdGVkX1/7+GLNZ8n/JzMwCZ7tncsy6gpMYdCkXms="
#---------------------------------------------------------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", electives=ELECTIVES)



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

#update these 2 ---------------------------------------------------------------------------------------------------------------------------------
# returns the house main room details
@app.route("/house_room/<house_id>", methods=['GET', 'POST'])
# returns the rooms that the house has
def home_rooms(house_id):
    key = secrets.token_bytes(32)
    print(type(key))
    print(key)

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
        # rooms = jsonify(rooms);
        rooms = str(rooms).encode()
        rooms = encrypt(rooms,password)
        return rooms
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
        result = str(result).encode()
        result = encrypt(result, password)
        return result
    else:
        return str(house_id)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

# needed for home page
@app.route("/average_temperature_house/<house_id>", methods=['GET'])
def average_temperature(house_id):
    # get the average temperature of the house
    result = {
        "temperature": 30,  # return as int
    }
    if house_id == "1234567":
        result = str(result).encode()
        result = encrypt(result, password)
        return result
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
        return result
    else:
        return str(house_id)


app.run(debug=True)
