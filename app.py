from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from werkzeug.utils import secure_filename
from model import predict_density   # Import function from model.py

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT,
                    density TEXT,
                    diagnosis TEXT,
                    notes TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    role = request.form["role"]
    session["role"] = role
    if role == "radiologist":
        return redirect(url_for("radiologist_dashboard"))
    elif role == "doctor":
        return redirect(url_for("doctor_dashboard"))
    return redirect(url_for("home"))

@app.route("/radiologist")
def radiologist_dashboard():
    return render_template("radiologist.html")

@app.route("/doctor")
def doctor_dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    reports = c.fetchall()
    conn.close()
    return render_template("doctor.html", reports=reports)

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return "No file uploaded"
    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Call ML model
    density = predict_density(filepath)

    return render_template("radiologist.html", density=density, image=filename)

@app.route("/submit_report", methods=["POST"])
def submit_report():
    patient_name = request.form["patient_name"]
    density = request.form["density"]
    diagnosis = request.form["diagnosis"]
    notes = request.form["notes"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO reports (patient_name, density, diagnosis, notes) VALUES (?, ?, ?, ?)",
              (patient_name, density, diagnosis, notes))
    conn.commit()
    conn.close()

    return redirect(url_for("doctor_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)