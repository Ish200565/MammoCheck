# 🚀 Complete Setup Instructions - MammoCheck with Google OAuth

## Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Environment File
```bash
copy .env.example .env
```

### Step 3: Configure Google OAuth

**Get Google Credentials:**
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add redirect URI: `http://127.0.0.1:5000/login/google/callback`

**Update .env file:**
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

📖 **Detailed instructions:** See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

### Step 4: Configure Email (Optional)

For appointment email notifications, configure email settings in `.env`:

```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

📖 **Detailed instructions:** See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)

### Step 5: Run Application
```bash
python app.py
```

### Step 6: Access Application
Open browser: `http://127.0.0.1:5000`

---

## Features Overview

### 🔐 Authentication
- **Google OAuth Login** - Secure one-click login
- **Traditional Login** - Role-based login (Doctor/Radiologist)
- **Session Management** - Persistent login tracking
- **Automatic Profile** - Name, email, and picture from Google

### 📧 Appointment Management
- Schedule patient appointments
- Send bulk email confirmations (10-20+ patients)
- Track email delivery status
- Manage appointments (add/delete)

### 🔬 Medical Features
- Upload mammogram images
- AI-powered density prediction
- Submit patient reports
- View all patient reports

---

## User Roles

### Doctor
- View patient reports
- Manage appointments
- Send email notifications
- Access patient data

### Radiologist
- Upload mammogram images
- Analyze breast density
- Submit medical reports
- Review analysis results

---

## Application Routes

| URL | Description | Login Required |
|-----|-------------|----------------|
| `/` | Login page | No |
| `/login/google` | Google OAuth login | No |
| `/logout` | Logout | Yes |
| `/doctor` | Doctor dashboard | Yes |
| `/radiologist` | Radiologist dashboard | Yes |
| `/appointments` | Appointment management | Yes |

---

## Database Tables

### users
Stores Google OAuth user information
- google_id, email, name, picture
- role (doctor/radiologist)
- created_at, last_login

### appointments
Manages patient appointments
- patient info, appointment details
- email_sent status

### reports
Stores medical reports
- patient_name, density, diagnosis, notes

---

## Project Structure

```
MammoCheck/
├── app.py                          # Main application
├── model.py                        # ML model
├── requirements.txt                # Dependencies
├── .env                           # Configuration (CREATE THIS)
├── .env.example                   # Configuration template
│
├── utils/
│   └── email_service.py          # Email functions
│
├── templates/
│   ├── login.html                # Login with Google button
│   ├── doctor.html               # Doctor dashboard
│   ├── radiologist.html          # Radiologist dashboard
│   └── appointments.html         # Appointment management
│
├── static/
│   ├── css/
│   │   └── style.css            # Styling
│   ├── js/
│   │   └── appointments.js      # Client-side logic
│   └── uploads/                 # Uploaded images
│
└── docs/
    ├── GOOGLE_OAUTH_SETUP.md    # Complete OAuth guide
    ├── EMAIL_SETUP_GUIDE.md     # Email configuration
    ├── GOOGLE_OAUTH_QUICKREF.md # Quick reference
    └── QUICK_START.md           # Quick start guide
```

---

## Configuration Files

### .env (Required)
```env
# Google OAuth (Required for Google login)
GOOGLE_CLIENT_ID=your-id
GOOGLE_CLIENT_SECRET=your-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/login/google/callback

# Email (Optional for appointment emails)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

---

## Testing Checklist

### Google OAuth
- [ ] Google Cloud project created
- [ ] OAuth credentials configured
- [ ] `.env` file created with credentials
- [ ] Click "Sign in with Google" works
- [ ] User info displayed after login
- [ ] Logout works
- [ ] User saved in database

### Email System
- [ ] Email credentials in `.env`
- [ ] Appointment added successfully
- [ ] Email sent to test address
- [ ] Email received (check spam folder)
- [ ] Multiple emails sent at once
- [ ] Email status tracked correctly

### Medical Features
- [ ] Image upload works
- [ ] Density prediction displays
- [ ] Report submission successful
- [ ] Reports visible in doctor dashboard

---

## Common Issues & Solutions

### "redirect_uri_mismatch"
**Solution:** Add exact redirect URI to Google Console:
- `http://127.0.0.1:5000/login/google/callback`
- `http://localhost:5000/login/google/callback`

### "This app isn't verified"
**Solution:** Click "Advanced" → "Go to MammoCheck (unsafe)"
This is normal for development mode.

### "ModuleNotFoundError"
**Solution:** 
```bash
pip install -r requirements.txt
```

### Email not sending
**Solution:**
1. Check `.env` file has correct credentials
2. Use Gmail App Password (not regular password)
3. Enable 2FA on Gmail first
4. Check spam folder

### Can't see user profile
**Solution:**
- Login using Google OAuth (not traditional login)
- Profile only shows for Google login users

---

## Development Tips

### View Database Content
```bash
# Install SQLite browser or use command line
sqlite3 database.db

# View users
SELECT * FROM users;

# View appointments
SELECT * FROM appointments;

# View reports
SELECT * FROM reports;
```

### Reset Database
```bash
# Delete database file
del database.db

# Restart app - new database created automatically
python app.py
```

### Update User Role
```python
# In Python REPL or script
import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("UPDATE users SET role = 'radiologist' WHERE email = 'user@example.com'")
conn.commit()
conn.close()
```

---

## Security Best Practices

✅ **DO:**
- Keep `.env` file secure
- Add `.env` to `.gitignore`
- Use HTTPS in production
- Rotate credentials regularly
- Use App Passwords for email
- Limit OAuth scopes

❌ **DON'T:**
- Commit `.env` to Git
- Share client secrets
- Use regular password for email
- Hardcode credentials
- Give unnecessary permissions

---

## Production Deployment

### Before Going Live:

1. **Update OAuth Settings**
   - Add production domain to authorized redirect URIs
   - Publish OAuth consent screen

2. **Environment Variables**
   - Update `.env` with production URLs
   - Use secure secret key

3. **Security**
   - Enable HTTPS
   - Use strong passwords
   - Enable CSRF protection
   - Secure session cookies

4. **Database**
   - Consider PostgreSQL/MySQL
   - Set up backups
   - Use migrations

---

## Documentation

| Document | Purpose |
|----------|---------|
| README.md | Overview and features |
| GOOGLE_OAUTH_SETUP.md | Complete OAuth walkthrough |
| GOOGLE_OAUTH_QUICKREF.md | Quick reference guide |
| EMAIL_SETUP_GUIDE.md | Email configuration |
| QUICK_START.md | Fast setup guide |

---

## Support & Resources

### Google OAuth
- Console: https://console.cloud.google.com/
- Documentation: https://developers.google.com/identity/protocols/oauth2

### Flask
- Documentation: https://flask.palletsprojects.com/
- Flask-Mail: https://pythonhosted.org/Flask-Mail/

### Authlib
- Documentation: https://docs.authlib.org/

---

## Next Steps

After setup:
1. ✅ Test Google login
2. ✅ Add test appointments
3. ✅ Send test emails
4. ✅ Upload test image
5. ✅ Create test reports
6. 🚀 Customize for your needs
7. 🚀 Deploy to production

---

**You're all set! Enjoy using MammoCheck! 🎉**

For detailed help, refer to:
- [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) - Step-by-step OAuth setup
- [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) - Email configuration
- [GOOGLE_OAUTH_QUICKREF.md](GOOGLE_OAUTH_QUICKREF.md) - Quick reference
