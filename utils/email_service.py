"""
Email Service Module
Handles sending appointment confirmation emails to patients
"""
from flask_mail import Message
from flask import render_template


def send_appointment_email(mail, recipient_email, patient_name, appointment_date, appointment_time, doctor_name):
    """
    Send appointment confirmation email to a single patient
    
    Args:
        mail: Flask-Mail instance
        recipient_email: Patient's email address
        patient_name: Patient's name
        appointment_date: Date of appointment
        appointment_time: Time of appointment
        doctor_name: Name of the doctor
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject="Appointment Confirmation - MammoCheck",
            recipients=[recipient_email]
        )
        
        # Email body
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">
                        Appointment Confirmation
                    </h2>
                    <p style="font-size: 16px; color: #34495e;">Dear <strong>{patient_name}</strong>,</p>
                    <p style="font-size: 14px; color: #7f8c8d; line-height: 1.6;">
                        Your appointment has been successfully booked at MammoCheck.
                    </p>
                    <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 10px 0;"><strong>Date:</strong> {appointment_date}</p>
                        <p style="margin: 10px 0;"><strong>Time:</strong> {appointment_time}</p>
                        <p style="margin: 10px 0;"><strong>Doctor:</strong> Dr. {doctor_name}</p>
                    </div>
                    <p style="font-size: 14px; color: #7f8c8d; line-height: 1.6;">
                        Please arrive 15 minutes before your scheduled time. If you need to reschedule, 
                        please contact us at least 24 hours in advance.
                    </p>
                    <p style="font-size: 14px; color: #7f8c8d; margin-top: 30px;">
                        Best regards,<br>
                        <strong>MammoCheck Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")
        return False


def send_bulk_appointment_emails(mail, appointments):
    """
    Send appointment confirmation emails to multiple patients
    
    Args:
        mail: Flask-Mail instance
        appointments: List of dict containing appointment details
                     Each dict should have: email, name, date, time, doctor
    
    Returns:
        dict: Results with success and failed counts
    """
    results = {
        'success': 0,
        'failed': 0,
        'failed_emails': []
    }
    
    for appointment in appointments:
        success = send_appointment_email(
            mail=mail,
            recipient_email=appointment['email'],
            patient_name=appointment['name'],
            appointment_date=appointment['date'],
            appointment_time=appointment['time'],
            doctor_name=appointment['doctor']
        )
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
            results['failed_emails'].append(appointment['email'])
    
    return results
