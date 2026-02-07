from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import sqlite3
from werkzeug.utils import secure_filename
from model import predict_density   # Import function from model.py
from flask_mail import Mail
from dotenv import load_dotenv
from utils.email_service import send_bulk_appointment_emails
from authlib.integrations.flask_client import OAuth
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    # Reports table
    c.execute("""CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT,
                    density TEXT,
                    diagnosis TEXT,
                    notes TEXT
                )""")
    
    # Appointments table
    c.execute("""CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT NOT NULL,
                    patient_email TEXT NOT NULL,
                    appointment_date TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    doctor_name TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    email_sent INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
    
    # Users table for Google OAuth
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    google_id TEXT UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    name TEXT,
                    picture TEXT,
                    role TEXT DEFAULT 'doctor',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    session["user_email"] = request.form.get("email", "guest@mammocheck.com")
    if role == "radiologist":
        return redirect(url_for("radiologist_dashboard"))
    elif role == "doctor":
        return redirect(url_for("doctor_dashboard"))
    return redirect(url_for("home"))

# Google OAuth Routes
@app.route("/login/google")
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/login/google/callback")
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Get access token from Google
        token = google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if user_info:
            google_id = user_info.get('sub')
            email = user_info.get('email')
            name = user_info.get('name')
            picture = user_info.get('picture')
            
            # Store or update user in database
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            
            # Check if user exists
            c.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
            existing_user = c.fetchone()
            
            if existing_user:
                # Update last login
                c.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE google_id = ?", (google_id,))
                role = existing_user[5]  # Role is at index 5
            else:
                # Create new user (default role: doctor)
                c.execute("""INSERT INTO users (google_id, email, name, picture, role) 
                            VALUES (?, ?, ?, ?, ?)""",
                          (google_id, email, name, picture, 'doctor'))
                role = 'doctor'
            
            conn.commit()
            conn.close()
            
            # Set session variables
            session['user_id'] = google_id
            session['user_email'] = email
            session['user_name'] = name
            session['user_picture'] = picture
            session['role'] = role
            session['logged_in_with_google'] = True
            
            flash(f"Welcome, {name}!", "success")
            
            # Redirect based on role
            if role == "radiologist":
                return redirect(url_for("radiologist_dashboard"))
            else:
                return redirect(url_for("doctor_dashboard"))
        else:
            flash("Failed to get user information from Google.", "error")
            return redirect(url_for("home"))
            
    except Exception as e:
        flash(f"Login failed: {str(e)}", "error")
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    """Logout user and clear session"""
    session.clear()
    flash("You have been logged out successfully.", "success")
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


# --- Appointment Management Routes ---
@app.route("/appointments")
def appointments_page():
    """Display appointment management page"""
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM appointments ORDER BY appointment_date, appointment_time")
    appointments = c.fetchall()
    conn.close()
    return render_template("appointments.html", appointments=appointments)


@app.route("/add_appointment", methods=["POST"])
def add_appointment():
    """Add a new appointment to the database"""
    try:
        patient_name = request.form["patient_name"]
        patient_email = request.form["patient_email"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        doctor_name = request.form["doctor_name"]
        
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""INSERT INTO appointments 
                    (patient_name, patient_email, appointment_date, appointment_time, doctor_name) 
                    VALUES (?, ?, ?, ?, ?)""",
                  (patient_name, patient_email, appointment_date, appointment_time, doctor_name))
        conn.commit()
        conn.close()
        
        flash("Appointment added successfully!", "success")
    except Exception as e:
        flash(f"Error adding appointment: {str(e)}", "error")
    
    return redirect(url_for("appointments_page"))


@app.route("/delete_appointment/<int:appointment_id>", methods=["POST"])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
        conn.close()
        flash("Appointment deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting appointment: {str(e)}", "error")
    
    return redirect(url_for("appointments_page"))


@app.route("/send_appointment_emails", methods=["POST"])
def send_appointment_emails():
    """Send confirmation emails to selected appointments"""
    try:
        selected_ids = request.form.getlist("selected_appointments")
        
        if not selected_ids:
            flash("Please select at least one appointment to send emails.", "warning")
            return redirect(url_for("appointments_page"))
        
        # Fetch selected appointments from database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        placeholders = ','.join('?' * len(selected_ids))
        c.execute(f"SELECT * FROM appointments WHERE id IN ({placeholders})", selected_ids)
        appointments_data = c.fetchall()
        
        # Prepare appointment data for email sending
        appointments = []
        for apt in appointments_data:
            appointments.append({
                'id': apt[0],
                'name': apt[1],
                'email': apt[2],
                'date': apt[3],
                'time': apt[4],
                'doctor': apt[5]
            })
        
        # Send bulk emails
        results = send_bulk_appointment_emails(mail, appointments)
        
        # Update email_sent status for successful emails
        if results['success'] > 0:
            successful_ids = [apt['id'] for apt in appointments if apt['email'] not in results['failed_emails']]
            if successful_ids:
                placeholders = ','.join('?' * len(successful_ids))
                c.execute(f"UPDATE appointments SET email_sent = 1 WHERE id IN ({placeholders})", successful_ids)
                conn.commit()
        
        conn.close()
        
        # Show results to user
        if results['failed'] == 0:
            flash(f"Successfully sent {results['success']} appointment confirmation emails!", "success")
        else:
            flash(f"Sent {results['success']} emails. Failed to send {results['failed']} emails.", "warning")
        
    except Exception as e:
        flash(f"Error sending emails: {str(e)}", "error")
    
    return redirect(url_for("appointments_page"))


if __name__ == "__main__":
    app.run(debug=True)