# 🔧 Google OAuth Troubleshooting Guide

## Quick Fixes for Common Issues

---

## ❌ Error: "redirect_uri_mismatch"

### Problem
```
Error 400: redirect_uri_mismatch
The redirect URI in the request doesn't match a registered redirect URI
```

### Solution
1. **Go to Google Cloud Console**
   - https://console.cloud.google.com/apis/credentials

2. **Edit OAuth 2.0 Client ID**
   - Click on your client ID

3. **Add Authorized Redirect URIs** (exact match required!)
   ```
   http://127.0.0.1:5000/login/google/callback
   http://localhost:5000/login/google/callback
   ```

4. **Save and Try Again**

### Common Mistakes
- Missing `http://` prefix
- Wrong port number (must be 5000)
- Typo in URL
- Extra spaces in URI

---

## ❌ Error: "This app isn't verified"

### Problem
```
Google OAuth warning:
"This app hasn't been verified by Google"
```

### Solution
**For Development (Recommended):**
1. Click "Advanced"
2. Click "Go to MammoCheck (unsafe)"
3. Continue with login

This is **normal** for apps in testing mode!

**For Production:**
- Submit app for Google verification
- Or publish to "In Production" status

### Why This Happens
- App is in "Testing" mode
- Google hasn't verified the app
- Normal for development/testing

---

## ❌ Error: "Error 403: access_denied"

### Problem
```
Error 403: access_denied
The app is in testing mode
```

### Solution
1. **Go to OAuth Consent Screen**
   - https://console.cloud.google.com/apis/credentials/consent

2. **Add Test Users**
   - Click "Add Users"
   - Enter the Google email addresses that need access
   - Save

3. **Alternative: Publish App**
   - Change status from "Testing" to "In Production"
   - (Only if ready for production)

---

## ❌ Error: "ModuleNotFoundError: No module named 'authlib'"

### Problem
```python
ModuleNotFoundError: No module named 'authlib'
```

### Solution
```bash
# Install missing packages
pip install authlib requests

# Or install all requirements
pip install -r requirements.txt
```

### Verify Installation
```bash
python -c "import authlib; print(authlib.__version__)"
```

---

## ❌ Error: "GOOGLE_CLIENT_ID not found"

### Problem
```python
KeyError: 'GOOGLE_CLIENT_ID'
# or
TypeError: 'NoneType' object is not iterable
```

### Solution
1. **Check .env file exists**
   ```bash
   # Windows
   dir .env
   
   # If not found, create it
   copy .env.example .env
   ```

2. **Verify .env contents**
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/login/google/callback
   ```

3. **Check for typos**
   - No extra spaces
   - Correct variable names
   - No quotes around values (unless part of the value)

4. **Restart application**
   ```bash
   python app.py
   ```

---

## ❌ Error: "Invalid client"

### Problem
```
Error: invalid_client
The OAuth client was not found
```

### Solution
1. **Verify credentials in .env**
   - Client ID should look like: `xxxxx.apps.googleusercontent.com`
   - Client Secret should look like: `GOCSPX-xxxxx`

2. **Copy fresh credentials**
   - Go to Google Cloud Console
   - Credentials page
   - Click on your OAuth 2.0 Client ID
   - Copy Client ID and Secret again

3. **Update .env file**
   - Paste new credentials
   - Save file
   - Restart app

---

## ❌ Can't Access Login Page

### Problem
- Browser shows "This site can't be reached"
- Connection refused

### Solution
1. **Check if Flask is running**
   ```bash
   python app.py
   ```
   Should show:
   ```
   * Running on http://127.0.0.1:5000
   ```

2. **Check correct URL**
   - Use: `http://127.0.0.1:5000`
   - Not: `https://...`
   - Not: `http://localhost:5000` (if 127.0.0.1 is configured)

3. **Check port availability**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   ```

4. **Try different port**
   ```python
   # In app.py
   if __name__ == "__main__":
       app.run(debug=True, port=5001)
   ```

---

## ❌ Google Login Button Not Working

### Problem
- Button click does nothing
- No redirect to Google

### Solution
1. **Check browser console**
   - Press F12
   - Check Console tab for JavaScript errors

2. **Verify route exists**
   ```python
   # In app.py
   @app.route("/login/google")
   def google_login():
       ...
   ```

3. **Check template**
   ```html
   <a href="{{ url_for('google_login') }}" ...>
   ```

4. **Clear browser cache**
   - Ctrl + Shift + Delete
   - Clear cached files

---

## ❌ User Profile Not Showing After Login

### Problem
- No profile picture or name displayed
- Dashboard shows but no user info

### Solution
1. **Ensure logged in with Google**
   - Traditional login doesn't provide profile info
   - Use "Sign in with Google" button

2. **Check session variables**
   ```python
   # Add to route to debug
   print(session.get('user_name'))
   print(session.get('user_picture'))
   print(session.get('logged_in_with_google'))
   ```

3. **Verify template code**
   ```html
   {% if session.get('logged_in_with_google') %}
       {{ session.user_name }}
   {% endif %}
   ```

---

## ❌ "500 Internal Server Error"

### Problem
- Server error after Google callback
- Can't complete login

### Solution
1. **Check Flask console for errors**
   - Look for Python tracebacks
   - Note the error type and line number

2. **Common causes:**
   - Database connection error
   - Missing database table
   - Session configuration issue

3. **Verify database**
   ```bash
   # Check if database.db exists
   dir database.db
   
   # Recreate if needed
   del database.db
   python app.py  # Creates new database
   ```

4. **Check app.py for errors**
   ```python
   # Ensure init_db() runs
   init_db()
   ```

---

## ❌ Session Lost After Refresh

### Problem
- User logout automatically
- Session doesn't persist

### Solution
1. **Check secret key**
   ```python
   # In app.py
   app.secret_key = "some-long-random-string"
   ```

2. **Use permanent sessions**
   ```python
   from datetime import timedelta
   
   app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
   
   # In login route
   session.permanent = True
   ```

---

## ❌ Multiple Users Getting Same Session

### Problem
- Wrong user information displayed
- User A sees User B's data

### Solution
1. **Clear all sessions**
   ```bash
   # Delete Flask session files
   # or restart app
   ```

2. **Use incognito/private browsing for testing**

3. **Check session uniqueness**
   ```python
   # Each user should have unique google_id
   session['user_id'] = user_info.get('sub')
   ```

---

## 🔍 Debugging Tools

### Enable Debug Mode
```python
# In app.py
if __name__ == "__main__":
    app.run(debug=True)
```

### Print Session Data
```python
@app.route("/debug/session")
def debug_session():
    return str(dict(session))
```

### Check Database Content
```bash
sqlite3 database.db
sqlite> .tables
sqlite> SELECT * FROM users;
sqlite> .quit
```

### Test OAuth Config
```python
# In Python REPL
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('GOOGLE_CLIENT_ID'))
print(os.getenv('GOOGLE_CLIENT_SECRET'))
```

---

## 📝 Verification Checklist

Use this checklist to verify your setup:

- [ ] Google Cloud project created
- [ ] APIs enabled (Google+, Identity Services)
- [ ] OAuth consent screen configured
- [ ] OAuth 2.0 credentials created
- [ ] Redirect URIs added correctly
- [ ] Test users added (for testing mode)
- [ ] `.env` file created from `.env.example`
- [ ] Client ID added to `.env`
- [ ] Client Secret added to `.env`
- [ ] No typos in credentials
- [ ] Required packages installed (`pip install -r requirements.txt`)
- [ ] Flask app running without errors
- [ ] Can access login page
- [ ] Google button redirects to Google
- [ ] Can complete Google login flow
- [ ] User info displayed after login
- [ ] User saved in database

---

## 🆘 Still Having Issues?

### Check These Resources

1. **Google Cloud Console**
   - https://console.cloud.google.com/
   - Check for API errors or quota issues

2. **Flask Console Output**
   - Look for Python errors and tracebacks
   - Note specific error messages

3. **Browser Console (F12)**
   - Check for JavaScript errors
   - Look at Network tab for failed requests

4. **Documentation**
   - [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)
   - [OAUTH_FLOW_DIAGRAM.md](OAUTH_FLOW_DIAGRAM.md)
   - [SETUP_COMPLETE.md](SETUP_COMPLETE.md)

### Common Error Log Locations
```
Flask console output (where you run python app.py)
Browser console (F12 → Console tab)
database.db (check if created and populated)
```

---

## 💡 Pro Tips

1. **Use Incognito Mode for Testing**
   - Prevents session conflicts
   - Fresh environment each time

2. **Keep Credentials Secure**
   - Never commit `.env` to Git
   - Use `.gitignore`

3. **Test with Multiple Accounts**
   - Add multiple test users
   - Verify role assignment works

4. **Monitor Google Cloud Console**
   - Check usage quotas
   - Monitor for errors

5. **Regular Credential Rotation**
   - Update secrets periodically
   - Generate new credentials if compromised

---

**Need more help? Review the complete setup guide in [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)!**
