"""
Email Configuration Test Script
Run this script to verify your email setup is working correctly
"""

from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path to import email service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.email_service import send_appointment_email, validate_email

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure email
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_configuration():
    """Check if email configuration is complete"""
    print_banner("📧 Email Configuration Check")
    
    config_items = {
        'MAIL_SERVER': os.getenv('MAIL_SERVER'),
        'MAIL_PORT': os.getenv('MAIL_PORT'),
        'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS'),
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER')
    }
    
    all_configured = True
    
    for key, value in config_items.items():
        if value:
            # Mask password for security
            display_value = value if key != 'MAIL_PASSWORD' else '*' * len(value)
            print(f"✓ {key}: {display_value}")
        else:
            print(f"✗ {key}: NOT SET")
            all_configured = False
    
    return all_configured

def test_email_validation():
    """Test email validation function"""
    print_banner("🔍 Testing Email Validation")
    
    test_emails = [
        ("valid@example.com", True),
        ("user.name@domain.co.uk", True),
        ("invalid.email", False),
        ("@domain.com", False),
        ("user@", False),
        ("user name@domain.com", False)
    ]
    
    all_passed = True
    
    for email, should_be_valid in test_emails:
        is_valid = validate_email(email)
        status = "✓" if is_valid == should_be_valid else "✗"
        expected = "Valid" if should_be_valid else "Invalid"
        print(f"{status} {email:30} -> {expected}")
        if is_valid != should_be_valid:
            all_passed = False
    
    return all_passed

def send_test_email():
    """Send a test email"""
    print_banner("📨 Sending Test Email")
    
    # Get recipient email from user
    recipient = input("Enter your email address to receive test email: ").strip()
    
    if not recipient:
        print("✗ No email address provided. Skipping test email.")
        return False
    
    if not validate_email(recipient):
        print(f"✗ Invalid email format: {recipient}")
        return False
    
    print(f"\nSending test email to: {recipient}")
    print("Please wait...")
    
    with app.app_context():
        success, error_msg = send_appointment_email(
            mail=mail,
            recipient_email=recipient,
            patient_name="Test Patient",
            appointment_date="2026-02-15",
            appointment_time="10:30 AM",
            doctor_name="Test Doctor"
        )
    
    if success:
        print("\n✓ Test email sent successfully!")
        print(f"  Check your inbox: {recipient}")
        print("  (Also check your spam/junk folder)")
        return True
    else:
        print(f"\n✗ Failed to send test email")
        print(f"  Error: {error_msg}")
        return False

def main():
    """Main test function"""
    print("\n" + "🏥" * 30)
    print("  MammoCheck Email Configuration Test")
    print("🏥" * 30)
    
    # Step 1: Check configuration
    config_ok = check_configuration()
    
    if not config_ok:
        print("\n⚠️  Configuration incomplete!")
        print("Please update your .env file with all required email settings.")
        print("See EMAIL_SETUP_GUIDE.md for detailed instructions.")
        return
    
    print("\n✓ All configuration values are set!")
    
    # Step 2: Test email validation
    validation_ok = test_email_validation()
    
    if not validation_ok:
        print("\n⚠️  Email validation tests failed!")
        return
    
    print("\n✓ Email validation working correctly!")
    
    # Step 3: Send test email (optional)
    print("\nDo you want to send a test email? (y/n): ", end="")
    response = input().strip().lower()
    
    if response in ['y', 'yes']:
        email_ok = send_test_email()
        
        if email_ok:
            print("\n" + "="*60)
            print("  ✓ All tests passed!")
            print("  Your email configuration is working correctly.")
            print("  You can now send appointment confirmation emails.")
            print("="*60 + "\n")
        else:
            print("\n" + "="*60)
            print("  ⚠️  Test email failed")
            print("  Please check:")
            print("  1. Your email credentials in .env file")
            print("  2. For Gmail: Use App Password, not regular password")
            print("  3. Enable 2-Factor Authentication on Gmail")
            print("  4. Check firewall settings")
            print("="*60 + "\n")
    else:
        print("\n✓ Test completed (email test skipped)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
