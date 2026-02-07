# 📧 Email Setup Guide for MammoCheck

## Step-by-Step Email Configuration

### 1. Create Your `.env` File

Copy the `.env.example` file and create a new file named `.env` in the root directory:

```bash
copy .env.example .env
```

### 2. Configure Gmail for Sending Emails

#### Option A: Using Gmail (Recommended for testing)

1. **Enable 2-Factor Authentication on your Gmail account**
   - Go to your Google Account settings
   - Navigate to Security → 2-Step Verification
   - Enable 2-Step Verification

2. **Generate an App Password**
   - Go to Google Account → Security
   - Under "Signing in to Google," select "App passwords"
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → Type "MammoCheck"
   - Click Generate
   - Copy the 16-character password

3. **Update your `.env` file**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

#### Option B: Using Other Email Services

**Outlook/Hotmail:**
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

**Yahoo Mail:**
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access Appointment Management

1. Open your browser and go to: `http://127.0.0.1:5000`
2. Navigate to: `http://127.0.0.1:5000/appointments`

## 📋 How to Use the Email Feature

### Adding Appointments

1. Fill in the appointment form with:
   - Patient Name
   - Patient Email
   - Appointment Date
   - Appointment Time
   - Doctor Name

2. Click "Add Appointment"

### Sending Bulk Emails

1. **Select Multiple Appointments:**
   - Check the boxes next to appointments (up to 10-20 patients)
   - Or click "Select All" to choose all appointments

2. **Send Confirmation Emails:**
   - Click the "Send Confirmation Emails" button
   - Confirm the action
   - Wait for success message

3. **Check Email Status:**
   - Green "✓ Sent" badge: Email sent successfully
   - Yellow "⏳ Pending" badge: Email not yet sent

## 🔧 Troubleshooting

### Common Issues:

**1. "Authentication failed" error**
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled on your Gmail account

**2. "Connection refused" error**
- Check your MAIL_SERVER and MAIL_PORT settings
- Ensure your firewall isn't blocking SMTP connections

**3. Emails not being received**
- Check the spam/junk folder
- Verify the recipient email addresses are correct
- Test with your own email first

**4. "No module named 'flask_mail'" error**
- Run: `pip install Flask-Mail`
- Or: `pip install -r requirements.txt`

## 📁 Project Structure

```
MammoCheck/
├── app.py                      # Main Flask application with routes
├── model.py                    # ML model for density prediction
├── requirements.txt            # Python dependencies
├── .env                        # Email configuration (create this!)
├── .env.example               # Example email configuration
├── database.db                # SQLite database (auto-created)
├── utils/
│   └── email_service.py      # Email sending functions
├── templates/
│   ├── login.html            # Login page
│   ├── doctor.html           # Doctor dashboard
│   ├── radiologist.html      # Radiologist dashboard
│   └── appointments.html     # Appointment management page
└── static/
    ├── css/
    │   └── style.css         # Styling for all pages
    ├── js/
    │   └── appointments.js   # JavaScript for appointments
    └── uploads/              # Uploaded mammogram images
```

## 🎯 Features

✅ Add multiple patient appointments  
✅ Send bulk confirmation emails (10-20+ patients at once)  
✅ Track email sending status  
✅ Beautiful email templates with appointment details  
✅ Responsive design for mobile and desktop  
✅ Delete appointments  
✅ Select all/individual appointments  

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your App Password secure
- Use environment variables for sensitive data
- Consider using a dedicated email account for sending notifications

## 📧 Email Template

The confirmation emails include:
- Patient name
- Appointment date and time
- Doctor name
- Professional formatting with your branding
- Important instructions for patients

## 🚀 Next Steps

1. Test with 1-2 appointments first
2. Verify emails are being received
3. Check spam folder if needed
4. Scale up to 10-20 appointments
5. Customize email templates as needed

---

**Need Help?** Check the troubleshooting section or review your email service provider's SMTP documentation.
