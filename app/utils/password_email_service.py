import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_password_reset_email(recipient_email, otp_code, guardian_name=None):
    """
    Send password reset OTP email using SMTP
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
            print("PASSWORD RESET OTP EMAIL (Console Output)")
            print(f"TO: {recipient_email}")
            print(f"OTP CODE: {otp_code}")
            print(f"EXPIRES: 5 minutes")
            print("=" * 60)
            return True
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Password Reset - iCane Smart Cane"
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
                .warning {{ 
                    color: #ff6b6b; 
                    background: #fff5f5; 
                    padding: 10px; 
                    border-radius: 5px; 
                    border-left: 4px solid #ff6b6b;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>iCane: Smart Cane</h1>
                </div>
                <div class="content">
                    <h2>Password Reset Request</h2>
                    <p>Hello {guardian_name or 'User'},</p>
                    <p>You have requested to reset your password. Please use the following verification code:</p>
                    
                    <div class="otp-code">{otp_code}</div>
                    
                    <p>This verification code will expire in <strong>5 minutes</strong>.</p>
                    
                    <div class="warning">
                        <p><strong>Important:</strong> If you didn't request a password reset, please ignore this email and ensure your account is secure.</p>
                    </div>
                    
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
        iCane: Smart Cane - Password Reset
        
        Hello {guardian_name or 'User'},
        
        You have requested to reset your password.
        
        Your verification code is: {otp_code}
        
        This code will expire in 5 minutes.
        
        If you didn't request this code, please ignore this email and ensure your account is secure.
        
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
        
        print(f" Password reset OTP email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send password reset OTP email to {recipient_email}: {str(e)}")
        # Fallback to console output
        print("=" * 60)
        print("PASSWORD RESET OTP EMAIL (Fallback - SMTP Failed)")
        print(f"TO: {recipient_email}")
        print(f"OTP CODE: {otp_code}")
        print("=" * 60)
        return True