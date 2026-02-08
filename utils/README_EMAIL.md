# 📧 Email Service Documentation

## Overview
This email service module handles sending appointment confirmation emails to patients in the MammoCheck application.

## Features

### ✅ Single Email Sending
- Send individual appointment confirmation emails
- Professional HTML email templates
- Plain text fallback for compatibility
- Email validation

### ✅ Bulk Email Sending
- Send emails to multiple patients simultaneously
- Progress tracking with console output
- Rate limiting to avoid spam filters (500ms delay between emails)
- Detailed error reporting
- Success/failure statistics

### ✅ Email Design
- Modern, responsive HTML design
- Gradient headers with professional styling
- Clear appointment details table
- Important instructions and reminders
- What to bring checklist
- Plain text version included

## Usage

### 1. Configure Email Settings

Edit your `.env` file with your email credentials:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate an App Password (not your regular password)
3. Use the 16-character app password in `.env`

### 2. Using the Web Interface

1. **Access Appointments Page:**
   - Navigate to: `http://127.0.0.1:5000/appointments`

2. **Add Appointments:**
   - Fill in the form with patient details
   - Click "Add Appointment"

3. **Send Bulk Emails:**
   - Check boxes next to appointments you want to send emails for
   - Or click "Select All" to choose all appointments
   - Click "📧 Send Confirmation Emails"
   - Confirm the action

4. **Track Status:**
   - ✓ Sent - Email successfully delivered
   - ⏳ Pending - Email not yet sent

### 3. Programmatic Usage

#### Send Single Email

```python
from utils.email_service import send_appointment_email

success, error_msg = send_appointment_email(
    mail=mail,  # Flask-Mail instance
    recipient_email="patient@example.com",
    patient_name="John Doe",
    appointment_date="2026-02-15",
    appointment_time="10:30 AM",
    doctor_name="Smith"
)

if success:
    print("Email sent successfully!")
else:
    print(f"Failed to send email: {error_msg}")
```

#### Send Bulk Emails

```python
from utils.email_service import send_bulk_appointment_emails

appointments = [
    {
        'email': 'patient1@example.com',
        'name': 'John Doe',
        'date': '2026-02-15',
        'time': '10:30 AM',
        'doctor': 'Smith'
    },
    {
        'email': 'patient2@example.com',
        'name': 'Jane Smith',
        'date': '2026-02-15',
        'time': '11:00 AM',
        'doctor': 'Johnson'
    }
]

results = send_bulk_appointment_emails(mail, appointments)

print(f"Success: {results['success']}/{results['total']}")
print(f"Failed: {results['failed']}/{results['total']}")
if results['failed'] > 0:
    print(f"Failed emails: {results['failed_emails']}")
    print(f"Errors: {results['errors']}")
```

## Return Values

### Single Email
Returns a tuple: `(success: bool, error_message: str or None)`

### Bulk Email
Returns a dictionary:
```python
{
    'success': 15,           # Number of successful sends
    'failed': 2,             # Number of failed sends
    'total': 17,             # Total emails attempted
    'failed_emails': [],     # List of failed email addresses
    'errors': {}             # Dict of email -> error message
}
```

## Email Template

The email contains:
- **Header:** MammoCheck branding with gradient
- **Greeting:** Personalized with patient name
- **Appointment Details:** Date, time, and doctor in a styled box
- **Important Notes:** Arrival time and rescheduling policy
- **Instructions:** What to bring checklist
- **Footer:** Professional sign-off

## Features

### Email Validation
- Validates email format before sending
- Prevents sending to invalid addresses
- Returns error for malformed emails

### Rate Limiting
- Adds 500ms delay between emails
- Prevents spam filter triggers
- Maintains server reputation

### Error Handling
- Catches and logs all sending errors
- Provides detailed error messages
- Continues processing remaining emails on failure

### Progress Tracking
- Console output for each email sent
- Shows progress: [1/20], [2/20], etc.
- Summary statistics at completion

## Troubleshooting

### Common Issues

#### 1. Authentication Failed
**Problem:** Can't authenticate with email server

**Solutions:**
- For Gmail, use App Password not regular password
- Enable 2-Factor Authentication first
- Check MAIL_USERNAME and MAIL_PASSWORD in .env

#### 2. Connection Refused
**Problem:** Can't connect to SMTP server

**Solutions:**
- Check MAIL_SERVER and MAIL_PORT settings
- Verify firewall isn't blocking port 587
- Try MAIL_PORT=465 with SSL instead of TLS

#### 3. Emails Going to Spam
**Problem:** Emails arrive in spam folder

**Solutions:**
- Add delay between emails (already implemented)
- Use a verified domain sender
- Ask recipients to whitelist your address

#### 4. Module Not Found
**Problem:** `ModuleNotFoundError: No module named 'flask_mail'`

**Solution:**
```bash
pip install Flask-Mail
# or
pip install -r requirements.txt
```

## Testing

### Test with Your Own Email First

1. Add an appointment with your personal email
2. Send the confirmation email
3. Check your inbox (and spam folder)
4. Verify the email looks correct
5. Then proceed with real patient emails

### Preview Function

Use the preview function to see email content without sending:

```python
from utils.email_service import create_email_preview

preview = create_email_preview(
    patient_name="John Doe",
    appointment_date="2026-02-15",
    appointment_time="10:30 AM",
    doctor_name="Smith"
)

print(preview)
```

## Best Practices

1. **Test First:** Always test with your own email before sending to patients
2. **Verify Data:** Ensure patient emails are valid and correct
3. **Batch Wisely:** Send 10-20 emails at a time for best results
4. **Monitor Status:** Check success/failure rates regularly
5. **Handle Failures:** Follow up on failed emails manually
6. **Secure Credentials:** Never commit .env file to version control
7. **Use App Passwords:** For Gmail, always use app-specific passwords

## Security

- ✅ Credentials stored in .env file (not in code)
- ✅ .env file in .gitignore (won't be committed)
- ✅ Email validation prevents injection attacks
- ✅ Plain text fallback for security-conscious clients
- ✅ No sensitive patient data in email logs

## Performance

- **Single Email:** ~0.5-2 seconds per email
- **Bulk Sending:** ~1 second per email (with delay)
- **Recommended Batch Size:** 10-50 emails
- **Rate Limit:** 500ms delay between emails

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review EMAIL_SETUP_GUIDE.md for detailed setup
3. Verify .env configuration
4. Check Flask console for error messages

---

**Version:** 2.0  
**Last Updated:** February 7, 2026  
**Maintainer:** MammoCheck Team
