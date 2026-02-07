# 🔐 Google OAuth Login Setup Guide

## Complete Guide to Setting Up Google Login for MammoCheck

This guide will walk you through setting up Google OAuth authentication for your MammoCheck application.

---

## 📋 Prerequisites

- Google Account
- MammoCheck application installed
- Internet connection

---

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   - Click on the project dropdown at the top
   - Click "NEW PROJECT"
   - Enter project name: `MammoCheck` (or any name you prefer)
   - Click "CREATE"
   - Wait for the project to be created (takes a few seconds)

### Step 2: Enable Google+ API

1. **Navigate to APIs & Services**
   - In the left sidebar, go to: **APIs & Services** → **Library**
   - Or use this direct link: https://console.cloud.google.com/apis/library

2. **Enable Required APIs**
   - Search for "Google+ API" and click on it
   - Click "ENABLE"
   - Also search for "Google Identity Services" and enable it

### Step 3: Configure OAuth Consent Screen

1. **Go to OAuth Consent Screen**
   - Left sidebar: **APIs & Services** → **OAuth consent screen**
   - Or: https://console.cloud.google.com/apis/credentials/consent

2. **Choose User Type**
   - Select **External** (for testing with any Google account)
   - Click "CREATE"

3. **Fill in App Information**
   - **App name:** `MammoCheck`
   - **User support email:** Your email address
   - **App logo:** (Optional - upload if you have one)
   - **Application home page:** `http://127.0.0.1:5000`
   - **Authorized domains:** Leave empty for local development
   - **Developer contact email:** Your email address
   - Click "SAVE AND CONTINUE"

4. **Scopes**
   - Click "ADD OR REMOVE SCOPES"
   - Select these scopes:
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `openid`
   - Click "UPDATE"
   - Click "SAVE AND CONTINUE"

5. **Test Users** (For External app during testing)
   - Click "ADD USERS"
   - Add your email address and any test users
   - Click "ADD"
   - Click "SAVE AND CONTINUE"

6. **Summary**
   - Review your settings
   - Click "BACK TO DASHBOARD"

### Step 4: Create OAuth 2.0 Credentials

1. **Go to Credentials Page**
   - Left sidebar: **APIs & Services** → **Credentials**
   - Or: https://console.cloud.google.com/apis/credentials

2. **Create OAuth Client ID**
   - Click "CREATE CREDENTIALS" at the top
   - Select "OAuth client ID"

3. **Configure OAuth Client**
   - **Application type:** Select "Web application"
   - **Name:** `MammoCheck Web Client`
   
4. **Add Authorized Redirect URIs** (IMPORTANT!)
   - Under "Authorized redirect URIs", click "ADD URI"
   - Add: `http://127.0.0.1:5000/login/google/callback`
   - Add: `http://localhost:5000/login/google/callback`
   - Click "CREATE"

5. **Save Your Credentials**
   - A popup will appear with your credentials
   - **Copy the Client ID** (looks like: `xxxxx.apps.googleusercontent.com`)
   - **Copy the Client Secret** (looks like: `GOCSPX-xxxxx`)
   - Click "OK"

   ⚠️ **IMPORTANT:** Keep these credentials secure and never commit them to version control!

### Step 5: Configure Your Application

1. **Create/Update .env File**
   
   In your MammoCheck root directory, create a file named `.env`:
   
   ```bash
   # On Windows PowerShell
   copy .env.example .env
   
   # Or create manually
   notepad .env
   ```

2. **Add Google OAuth Credentials to .env**
   
   Open `.env` and add your credentials:
   
   ```env
   # Email Configuration (existing)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com

   # Google OAuth Configuration (ADD THESE)
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/login/google/callback
   ```

   Replace:
   - `your-client-id.apps.googleusercontent.com` with your actual Client ID
   - `your-client-secret` with your actual Client Secret

3. **Save the file** (DO NOT commit this file to Git!)

### Step 6: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `authlib` - OAuth library
- `requests` - HTTP library for API calls

### Step 7: Run Your Application

```bash
python app.py
```

### Step 8: Test Google Login

1. **Open your browser**
   - Go to: `http://127.0.0.1:5000`

2. **Click "Sign in with Google"**
   - You'll be redirected to Google's login page
   - Enter your Google credentials
   - Grant permissions to the app

3. **Success!**
   - You should be redirected back to your app
   - You'll be logged in and see the dashboard

---

## 🎯 How It Works

### User Flow:

1. User clicks "Sign in with Google" on login page
2. App redirects to Google OAuth consent screen
3. User logs in with Google and grants permissions
4. Google redirects back to app with authorization code
5. App exchanges code for access token
6. App retrieves user info (email, name, picture)
7. App stores/updates user in database
8. User is logged in and redirected to their dashboard

### Database Structure:

A new `users` table is created with:
- `google_id` - Unique Google user ID
- `email` - User's email from Google
- `name` - User's full name
- `picture` - Profile picture URL
- `role` - User role (doctor/radiologist)
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp

### Session Management:

When logged in with Google, the session contains:
- `user_id` - Google ID
- `user_email` - Email address
- `user_name` - Full name
- `user_picture` - Profile picture URL
- `role` - User role
- `logged_in_with_google` - Boolean flag

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. "Error 400: redirect_uri_mismatch"

**Problem:** The redirect URI doesn't match what's configured in Google Cloud Console.

**Solution:**
- Go to Google Cloud Console → Credentials
- Edit your OAuth 2.0 Client ID
- Make sure `http://127.0.0.1:5000/login/google/callback` is in the Authorized redirect URIs
- Also add `http://localhost:5000/login/google/callback`
- Save and try again

#### 2. "This app isn't verified"

**Problem:** Google shows a warning about unverified app.

**Solution:**
- This is normal for apps in testing mode
- Click "Advanced" → "Go to MammoCheck (unsafe)"
- For production, you'll need to submit for verification

#### 3. "Error 403: access_denied"

**Problem:** App is in testing mode and user isn't added as test user.

**Solution:**
- Go to OAuth consent screen in Google Cloud Console
- Add the user's email to "Test users"
- Or publish the app (change to External in production)

#### 4. "ModuleNotFoundError: No module named 'authlib'"

**Problem:** Required packages not installed.

**Solution:**
```bash
pip install authlib requests
# Or
pip install -r requirements.txt
```

#### 5. "GOOGLE_CLIENT_ID not found"

**Problem:** Environment variables not loaded.

**Solution:**
- Make sure `.env` file exists in root directory
- Check that values are correctly set
- Restart the Flask application

#### 6. Users Can't Login - "Invalid credentials"

**Problem:** Client ID or Secret is incorrect.

**Solution:**
- Verify credentials in Google Cloud Console
- Copy them again to `.env` file
- Make sure there are no extra spaces
- Restart the application

---

## 🔐 Security Best Practices

### DO:
✅ Keep your `.env` file secure and never commit it to Git  
✅ Use environment variables for sensitive data  
✅ Add `.env` to your `.gitignore` file  
✅ Use HTTPS in production  
✅ Regularly rotate your client secret  
✅ Limit OAuth scopes to only what you need  
✅ Add only necessary test users  

### DON'T:
❌ Never hardcode credentials in your code  
❌ Don't share your client secret publicly  
❌ Don't commit `.env` to version control  
❌ Don't use the same credentials for dev and production  
❌ Don't grant unnecessary permissions  

---

## 📱 User Management Features

### View Users:

Access the users in your database:

```python
# In Python/Flask
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("SELECT * FROM users")
users = c.fetchall()
conn.close()
```

### Update User Role:

To change a user's role from doctor to radiologist:

```python
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("UPDATE users SET role = 'radiologist' WHERE email = ?", (user_email,))
conn.commit()
conn.close()
```

### Logout:

Users can logout by visiting: `http://127.0.0.1:5000/logout`

---

## 🚀 Production Deployment

When deploying to production:

1. **Update Redirect URIs**
   - Add your production domain: `https://yourdomain.com/login/google/callback`
   - Update in Google Cloud Console

2. **Update .env for Production**
   ```env
   GOOGLE_REDIRECT_URI=https://yourdomain.com/login/google/callback
   ```

3. **Publish OAuth App**
   - Change from "Testing" to "In Production" in OAuth consent screen
   - Submit for verification if needed

4. **Use HTTPS**
   - Google OAuth requires HTTPS in production
   - Use SSL certificates

5. **Secure Your Environment**
   - Use a strong secret key for Flask
   - Enable CSRF protection
   - Use secure session cookies

---

## 📊 Features Available After Login

After successful Google login, users can:

- ✅ Access personalized dashboards based on role
- ✅ See their profile picture and name in the session
- ✅ Automatic role assignment (default: doctor)
- ✅ Persistent login tracking
- ✅ Seamless integration with existing features
- ✅ Logout functionality

---

## 🎨 Customization

### Change Default Role:

Edit `app.py`, line in `google_callback()` function:

```python
role = 'radiologist'  # Change default role here
```

### Add More User Fields:

Modify the `users` table in `app.py`:

```python
c.execute("""CREATE TABLE IF NOT EXISTS users (
    ...
    phone TEXT,
    department TEXT,
    ...
)""")
```

---

## 📞 Support

If you encounter issues:

1. Check this guide thoroughly
2. Review the Troubleshooting section
3. Check Google Cloud Console for error messages
4. Verify all credentials are correct
5. Check Flask application logs

---

## 🎉 Success!

You now have Google OAuth login working on your MammoCheck application!

Users can:
- Login with their Google account
- Get automatic profile information
- Access role-based dashboards
- Enjoy a seamless authentication experience

**Next Steps:**
- Test with multiple users
- Customize user roles as needed
- Add more features based on user roles
- Deploy to production when ready

---

**Happy Coding! 🚀**
