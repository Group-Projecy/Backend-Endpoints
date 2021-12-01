from flask import Flask, render_template, request, redirect, jsonify
import os


app = Flask(__name__)

user = {

}

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
    if content['email'] == email and content['password'] == password:
        result = {"Result": "True",
               "HouseID": "12345"
               }
        return result
    else:
        return "False"





app.run(debug=True)
