import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_otp_email(recipient_email, otp_code, guardian_name=None):
    """
    Send OTP verification email using SMTP
    """
    try:
        # Email configuration from environment variables
        smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('MAIL_PORT', 587))
        email_username = os.environ.get('MAIL_USERNAME', '')
        email_password = os.environ.get('MAIL_PASSWORD', '')
        sender_name = os.environ.get('MAIL_SENDER_NAME', 'iCane Smart Cane')
        
        # If no email credentials provided, fallback to console output
        if not email_username or not email_password:
            print("=" * 60)
            print("📧 OTP EMAIL (Console Output - Configure SMTP for real emails)")
            print(f"TO: {recipient_email}")
            print(f"OTP CODE: {otp_code}")
            print(f"EXPIRES: 10 minutes")
            print("=" * 60)
            return True
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Verify Your Email - iCane Smart Cane"
        msg['From'] = formataddr((sender_name, email_username))
        msg['To'] = recipient_email
        
        # HTML email content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1C253C; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .otp-code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    text-align: center; 
                    color: #1C253C;
                    letter-spacing: 5px;
                    margin: 20px 0;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    border: 2px dashed #1C253C;
                }}
                .footer {{ 
                    background: #ddd; 
                    padding: 15px; 
                    text-align: center; 
                    font-size: 12px; 
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>iCane Smart Cane</h1>
                </div>
                <div class="content">
                    <h2>Email Verification</h2>
                    <p>Hello {guardian_name or 'User'},</p>
                    <p>Please use the following verification code to complete your registration:</p>
                    
                    <div class="otp-code">{otp_code}</div>
                    
                    <p>This verification code will expire in <strong>10 minutes</strong>.</p>
                    
                    <p>If you didn't request this code, please ignore this email.</p>
                    
                    <p>Best regards,<br>iCane Smart Cane Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 iCane Smart Cane. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_content = f"""
        iCane Smart Cane - Email Verification
        
        Hello {guardian_name or 'User'},
        
        Your verification code is: {otp_code}
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        iCane Smart Cane Team
        """
        
        # Attach both HTML and plain text versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email_username, email_password)
            server.send_message(msg)
        
        print(f"✅ OTP email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send OTP email to {recipient_email}: {str(e)}")
        # Fallback to console output
        print("=" * 60)
        print("📧 OTP EMAIL (Fallback - SMTP Failed)")
        print(f"TO: {recipient_email}")
        print(f"OTP CODE: {otp_code}")
        print("=" * 60)
        return True  # Return True to continue registration process

def send_welcome_email(recipient_email, guardian_name):
    """
    Send welcome email after successful registration
    """
    try:
        # For now, just log to console
        print("=" * 60)
        print("🎉 WELCOME EMAIL")
        print(f"TO: {recipient_email}")
        print(f"GUARDIAN: {guardian_name}")
        print("Welcome to iCane Smart Cane!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        return True