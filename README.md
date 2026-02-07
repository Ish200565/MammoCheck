# MammoCheck

A medical healthcare web application for mammography density analysis with automated appointment email notifications.

## 🌟 Features

- **🔐 Google OAuth Login**: Secure authentication with Google accounts
- **Mammography Analysis**: Upload and analyze mammogram images with AI-powered density prediction
- **Radiologist Dashboard**: Interface for radiologists to review images and submit reports
- **Doctor Dashboard**: View patient reports and medical data
- **📧 Appointment Management**: Schedule patient appointments and send bulk email confirmations
- **Email Notifications**: Automatically send appointment confirmations to 10-20+ patients at once
- **Email Tracking**: Monitor which patients have received confirmation emails
- **User Management**: Automatic user profile creation with Google login

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Settings**
   ```bash
   copy .env.example .env
   # Edit .env with your email and Google OAuth credentials
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Main App: `http://127.0.0.1:5000`
   - Appointments: `http://127.0.0.1:5000/appointments`

## � Google Login Setup

The application supports Google OAuth authentication for secure user login.

**Quick Setup:**
1. Create a Google Cloud Project
2. Enable Google+ API
3. Create OAuth 2.0 credentials
4. Add credentials to `.env` file

**See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) for detailed step-by-step instructions.**

### Benefits:
- 🔒 Secure authentication
- 👤 Automatic profile creation
- 📧 Verified email addresses
- 🎨 Profile pictures
- ⚡ One-click login

## �📧 Email Feature

The appointment management system allows you to:
- Add multiple patient appointments
- Select 10-20 appointments at once
- Send bulk confirmation emails with a single click
- Track email delivery status
- Beautiful HTML email templates with appointment details

**See [QUICK_START.md](QUICK_START.md) and [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) for detailed instructions.**

## 📁 Project Structure

```
MammoCheck/
├── app.py                      # Main Flask application with all routes
├── model.py                    # ML model for density prediction
├── requirements.txt            # Python dependencies
├── .env                        # Email configuration (you create this)
├── .env.example               # Email configuration template
├── utils/with Google OAuth |
| `/login` | Traditional login |
| `/login/google` | Initiate Google OAuth |
| `/login/google/callback` | Google OAuth callback |
| `/logout` | Logout and clear sessl sending functionality
├── templates/
│   ├── login.html             # Login page
│   ├── doctor.html            # Doctor dashboard
│   ├── radiologist.html       # Radiologist dashboard
│   └── appointments.html      # Appointment management
└── static/
    ├── css/
    Authentication**: Google OAuth 2.0 (Authlib)
- **│   └── style.css          # Styling
    ├── js/
    │   └── appointments.js    # Appointment page scripts
    └── uploads/               # Uploaded images
```

## 🔗 Routes

- [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) - Complete Google OAuth setup walkthrough
| Route | Description |
|-------|-------------|
| `/` | Login page |
| `/login` | Handle login authentication |
| `/radiologist` | Radiologist dashboard |
| `/doctor` | Doctor dashboard with reports |
| 🔐 Secure user authentication with Google
- 📅 Schedule and manage mammography appointments
- 📧 Send appointment confirmations to multiple patients simultaneously
- 📊 Track patient appointments and email status
- 🔬 Analyze mammogram images for density assessment
- 📋 Generate and review medical reports
- 👥 Role-based access control (Doctor/Radiologist)
## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Email**: Flask-Mail
- **Frontend**: HTML, CSS, JavaScript
- **ML**: Custom density prediction model

## 📖 Documentation

- [QUICK_START.md](QUICK_START.md) - Get up and running in 5 minutes
- [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) - Detailed email configuration guide

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🎯 Use Cases

- Schedule and manage mammography appointments
- Send appointment confirmations to multiple patients simultaneously
- Track patient appointments and email status
- Analyze mammogram images for density assessment
- Generate and review medical reports