# 🚀 Quick Start Guide - Appointment Email System

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Email
1. Copy `.env.example` to create `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and add your email credentials:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

### Step 3: Run the Application
```bash
python app.py
```

## Usage

### Access the Appointment System
Open your browser and navigate to:
```
http://127.0.0.1:5000/appointments
```

### Send Emails to Multiple Patients

**Method 1: From Appointments Page**
1. Add patient appointments using the form
2. Select multiple appointments (checkboxes)
3. Click "Send Confirmation Emails"
4. Done! Emails sent to 10-20 patients at once

### Routes Available

| Route | Description |
|-------|-------------|
| `/` | Login page |
| `/radiologist` | Radiologist dashboard |
| `/doctor` | Doctor dashboard with reports |
| `/appointments` | **Appointment management & email sending** |

## Project Structure

```
MammoCheck/
├── 📄 app.py                    # Main Flask app (all routes here)
├── 📄 model.py                  # ML model functions
├── 📄 requirements.txt          # Dependencies
├── 📄 .env                      # Email config (YOU CREATE THIS)
├── 📄 .env.example             # Email config template
│
├── 📁 utils/                   # Utility functions
│   └── email_service.py        # Email sending logic
│
├── 📁 templates/               # HTML pages
│   ├── login.html
│   ├── doctor.html
│   ├── radiologist.html
│   └── appointments.html       # 📧 Email management page
│
└── 📁 static/                  # Static files
    ├── css/
    │   └── style.css          # All styling
    ├── js/
    │   └── appointments.js    # Appointment page logic
    └── uploads/               # Uploaded images
```

## Key Features

✅ **Bulk Email Sending**: Send to 10-20 patients simultaneously  
✅ **Email Status Tracking**: See which emails were sent  
✅ **Easy Management**: Add, view, and delete appointments  
✅ **Professional Emails**: Beautiful HTML email templates  
✅ **Responsive Design**: Works on desktop and mobile  

## Testing

**Test with your own email first:**
1. Add an appointment with your email address
2. Select it and send the confirmation
3. Check your inbox/spam folder
4. Once working, add more patient emails

## Email Configuration (Gmail)

**Quick Gmail Setup:**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Google Account → Security → App Passwords
3. Use the 16-character password in your `.env` file

**See EMAIL_SETUP_GUIDE.md for detailed instructions**

## Common Commands

```bash
# Install packages
pip install -r requirements.txt

# Run application
python app.py

# Access appointment page
# Browser: http://127.0.0.1:5000/appointments
```

## Need Help?

📖 **Detailed Setup**: See `EMAIL_SETUP_GUIDE.md`  
🐛 **Troubleshooting**: Check the troubleshooting section in EMAIL_SETUP_GUIDE.md  
🔧 **Routes**: All defined in `app.py` (lines 70-150)  

---

**You're all set!** Start by creating your `.env` file and test with 1-2 appointments. 🎉
