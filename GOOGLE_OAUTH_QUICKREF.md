# 🔐 Google OAuth - Quick Reference

## Installation Command
```bash
pip install -r requirements.txt
```

## Required Packages
- `authlib` - OAuth library
- `requests` - HTTP requests

## Environment Variables (.env)
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/login/google/callback
```

## Google Cloud Console URLs

| Action | URL |
|--------|-----|
| Cloud Console | https://console.cloud.google.com/ |
| Create Project | https://console.cloud.google.com/projectcreate |
| OAuth Consent | https://console.cloud.google.com/apis/credentials/consent |
| Credentials | https://console.cloud.google.com/apis/credentials |
| API Library | https://console.cloud.google.com/apis/library |

## Setup Checklist

- [ ] Created Google Cloud Project
- [ ] Enabled Google+ API
- [ ] Configured OAuth consent screen
- [ ] Created OAuth 2.0 Client ID
- [ ] Added authorized redirect URIs:
  - `http://127.0.0.1:5000/login/google/callback`
  - `http://localhost:5000/login/google/callback`
- [ ] Copied Client ID to .env
- [ ] Copied Client Secret to .env
- [ ] Installed required packages
- [ ] Tested Google login

## Application Routes

| Route | Purpose |
|-------|---------|
| `/` | Login page with Google button |
| `/login/google` | Start Google OAuth flow |
| `/login/google/callback` | Handle Google response |
| `/logout` | Logout user |

## Database Table: users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE,
    email TEXT NOT NULL UNIQUE,
    name TEXT,
    picture TEXT,
    role TEXT DEFAULT 'doctor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Session Variables (After Login)

```python
session['user_id']                  # Google ID
session['user_email']               # Email
session['user_name']                # Full name
session['user_picture']             # Profile picture URL
session['role']                     # 'doctor' or 'radiologist'
session['logged_in_with_google']    # True
```

## Common OAuth Scopes

```
openid                      # Required for OAuth
email                       # User's email
profile                     # Name, picture, etc.
```

## Testing Steps

1. Start application: `python app.py`
2. Open: `http://127.0.0.1:5000`
3. Click "Sign in with Google"
4. Login with Google
5. Grant permissions
6. Verify redirect to dashboard
7. Check user created in database

## Troubleshooting Quick Fixes

| Error | Quick Fix |
|-------|-----------|
| redirect_uri_mismatch | Add exact redirect URI to Google Console |
| access_denied | Add user email to test users |
| Module not found | Run `pip install authlib requests` |
| 404 on callback | Check route in app.py |
| No GOOGLE_CLIENT_ID | Create .env file with credentials |

## Production Checklist

- [ ] Use HTTPS
- [ ] Update redirect URI to production URL
- [ ] Publish OAuth consent screen
- [ ] Use strong secret key
- [ ] Enable CSRF protection
- [ ] Use secure session cookies
- [ ] Don't commit .env file
- [ ] Submit for verification (if needed)

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env from example
copy .env.example .env

# Run application
python app.py

# Check users in database
sqlite3 database.db "SELECT * FROM users;"
```

## Need Help?

📖 See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) for complete guide

---

**Remember:** Never commit your `.env` file or share your Client Secret! 🔒
