# 📊 Google OAuth Flow Diagram

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INITIATES LOGIN                          │
│                                                                   │
│  User clicks "Sign in with Google" button on login page         │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: AUTHORIZATION                         │
│                                                                   │
│  MammoCheck redirects to Google OAuth                           │
│  URL: /login/google                                             │
│  → Google Authorization Server                                   │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: USER CONSENT                          │
│                                                                   │
│  Google shows login page                                        │
│  User enters credentials                                         │
│  User grants permissions (email, profile)                        │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 3: CALLBACK                              │
│                                                                   │
│  Google redirects back to MammoCheck                            │
│  URL: /login/google/callback?code=...                           │
│  Contains authorization code                                     │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 4: TOKEN EXCHANGE                        │
│                                                                   │
│  MammoCheck exchanges code for access token                     │
│  Receives user information (email, name, picture)               │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 5: USER CREATION/UPDATE                  │
│                                                                   │
│  Check if user exists in database                               │
│  ├─ Exists: Update last_login                                   │
│  └─ New: Create user record                                     │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 6: SESSION CREATION                      │
│                                                                   │
│  Store user info in Flask session:                              │
│  - user_id (Google ID)                                          │
│  - user_email                                                    │
│  - user_name                                                     │
│  - user_picture                                                  │
│  - role (doctor/radiologist)                                    │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    STEP 7: REDIRECT TO DASHBOARD                 │
│                                                                   │
│  Based on user role:                                            │
│  ├─ Doctor → /doctor                                            │
│  └─ Radiologist → /radiologist                                  │
│                           ↓                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    USER IS LOGGED IN!                            │
│                                                                   │
│  - Profile picture displayed                                     │
│  - Name and email shown                                         │
│  - Access to dashboard features                                 │
│  - Session persists until logout                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Interaction

```
┌──────────────────────────────────────────────────────────────────┐
│                         DATABASE FLOW                             │
└──────────────────────────────────────────────────────────────────┘

Google User Info                    Database (users table)
─────────────────                   ──────────────────────
google_id: 123456        ──┐        
email: user@gmail.com      ├───→    Check if google_id exists?
name: John Doe             │                   │
picture: https://...     ──┘                   │
                                               ├─ YES: UPDATE last_login
                                               │
                                               └─ NO:  INSERT new user
                                                       - google_id
                                                       - email  
                                                       - name
                                                       - picture
                                                       - role (default: doctor)
                                                       - created_at
                                                       - last_login
```

---

## Session Management

```
┌─────────────────────────────────────────────────────────────┐
│                    FLASK SESSION STORAGE                     │
├─────────────────────────────────────────────────────────────┤
│  Key                        Value                           │
├──────────────────────────────────────────────────────────────
│  user_id                    "123456789"                     │
│  user_email                 "user@gmail.com"                │
│  user_name                  "John Doe"                      │
│  user_picture               "https://lh3.google..."         │
│  role                       "doctor"                        │
│  logged_in_with_google      True                            │
└─────────────────────────────────────────────────────────────┘

Available in templates as:
  {{ session.user_name }}
  {{ session.user_email }}
  {{ session.user_picture }}
```

---

## File Structure & Routes

```
MammoCheck Application
│
├── Route: /
│   ├── File: templates/login.html
│   ├── Shows: Login page with Google button
│   └── Button: "Sign in with Google" → /login/google
│
├── Route: /login/google
│   ├── File: app.py (google_login function)
│   ├── Action: Initiate OAuth flow
│   └── Redirect: Google Authorization Server
│
├── Route: /login/google/callback
│   ├── File: app.py (google_callback function)
│   ├── Action: Handle OAuth response
│   ├── Process: Get token, fetch user info
│   ├── Database: Create/update user
│   ├── Session: Store user data
│   └── Redirect: Dashboard based on role
│
├── Route: /doctor
│   ├── File: templates/doctor.html
│   ├── Shows: Doctor dashboard with reports
│   └── Profile: Displays Google user info
│
├── Route: /radiologist
│   ├── File: templates/radiologist.html
│   ├── Shows: Radiologist dashboard
│   └── Profile: Displays Google user info
│
└── Route: /logout
    ├── File: app.py (logout function)
    ├── Action: Clear session
    └── Redirect: Login page
```

---

## Security Flow

```
┌────────────────────────────────────────────────────────────┐
│                    SECURITY MEASURES                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ENVIRONMENT VARIABLES (.env)                           │
│     ├─ Client ID and Secret never hardcoded               │
│     └─ Sensitive data stored securely                     │
│                                                             │
│  2. OAUTH 2.0 PROTOCOL                                     │
│     ├─ Industry-standard authentication                    │
│     ├─ Encrypted communication with Google                │
│     └─ No password handling by our app                    │
│                                                             │
│  3. SESSION MANAGEMENT                                     │
│     ├─ Flask secure sessions                              │
│     ├─ Server-side session storage                        │
│     └─ Session cleared on logout                          │
│                                                             │
│  4. DATABASE SECURITY                                      │
│     ├─ No password storage                                │
│     ├─ Google ID as unique identifier                     │
│     └─ SQL injection protection (parameterized queries)   │
│                                                             │
│  5. SCOPE LIMITATION                                       │
│     ├─ Only request necessary permissions                 │
│     ├─ openid, email, profile only                        │
│     └─ No access to sensitive Google data                 │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Error Handling

```
Possible Issues & Error Flow
───────────────────────────────

1. redirect_uri_mismatch
   └─→ User sees error
       └─→ Fix: Add correct URI to Google Console

2. access_denied (User denies permission)
   └─→ Redirect to login page
       └─→ Show error message

3. Invalid credentials
   └─→ OAuth flow fails
       └─→ Redirect to login with error

4. Database error
   └─→ Catch exception
       └─→ Show error message
       └─→ Redirect to login

5. Session expired
   └─→ Check session on protected routes
       └─→ Redirect to login if not authenticated
```

---

## Feature Integration

```
┌────────────────────────────────────────────────────────────────┐
│             GOOGLE LOGIN INTEGRATED WITH FEATURES               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Appointments System                                           │
│  ├─ User email auto-filled from Google                        │
│  ├─ Appointment confirmations sent to verified email          │
│  └─ Creator identified by Google ID                           │
│                                                                 │
│  Medical Reports                                               │
│  ├─ Reports linked to user account                            │
│  ├─ Doctor name from Google profile                           │
│  └─ Audit trail with Google ID                                │
│                                                                 │
│  User Interface                                                │
│  ├─ Profile picture in header                                 │
│  ├─ Personalized greeting                                     │
│  ├─ Role-based navigation                                     │
│  └─ Logout button for Google users                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Commands

```bash
# View users who logged in with Google
sqlite3 database.db "SELECT email, name, role, last_login FROM users;"

# Count total Google users
sqlite3 database.db "SELECT COUNT(*) FROM users;"

# Update user role
sqlite3 database.db "UPDATE users SET role='radiologist' WHERE email='user@gmail.com';"

# View recent logins
sqlite3 database.db "SELECT name, email, last_login FROM users ORDER BY last_login DESC LIMIT 10;"
```

---

This diagram provides a comprehensive view of how Google OAuth integrates with MammoCheck!
