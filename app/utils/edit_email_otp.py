"""
Email template for edit profile email verification
"""

def get_edit_email_otp_template(recipient_email, otp_code, guardian_name, action="email_change"):
    """
    Generate OTP email template for email change verification
    
    Args:
        recipient_email (str): The recipient's email address
        otp_code (str): The OTP code
        guardian_name (str): The guardian's name
        action (str): Type of action - 'email_change' or 'profile_update'
    
    Returns:
        tuple: (subject, html_body, text_body)
    """
    
    if action == "email_change":
        subject = "Verify Your New Email Address - iCane"
        action_text = "change your email address"
    else:
        subject = "Verify Your Profile Update - iCane"
        action_text = "update your profile"
    
    # HTML email template
    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
            }}
            .header {{
                background: linear-gradient(135deg, #11285A 0%, #1a3a7a 100%);
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                color: white;
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 18px;
                color: #11285A;
                margin-bottom: 20px;
            }}
            .otp-container {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 12px;
                padding: 25px;
                margin: 30px 0;
                text-align: center;
                border: 2px solid #e0e7ff;
            }}
            .otp-code {{
                font-size: 42px;
                font-weight: 700;
                color: #11285A;
                letter-spacing: 8px;
                margin: 15px 0;
                font-family: 'Courier New', monospace;
            }}
            .instructions {{
                color: #666;
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 25px;
            }}
            .warning-box {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
            }}
            .warning-title {{
                color: #856404;
                font-weight: 600;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .warning-text {{
                color: #856404;
                font-size: 13px;
                margin: 0;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 25px 30px;
                text-align: center;
                border-top: 1px solid #e9ecef;
                border-radius: 0 0 10px 10px;
                color: #6c757d;
                font-size: 12px;
            }}
            .logo {{
                font-size: 20px;
                font-weight: 700;
                color: #11285A;
                margin-bottom: 10px;
            }}
            .support-info {{
                margin-top: 15px;
                font-size: 12px;
                color: #6c757d;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #11285A 0%, #1a3a7a 100%);
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Smart Cane Guardian</h1>
            </div>
            
            <div class="content">
                <div class="greeting">
                    Hello <strong>{guardian_name}</strong>,
                </div>
                
                <p>You have requested to {action_text} for your Smart Cane Guardian account.</p>
                <p>To complete this request, please use the verification code below:</p>
                
                <div class="otp-container">
                    <div style="font-size: 14px; color: #666; margin-bottom: 10px;">Your verification code:</div>
                    <div class="otp-code">{otp_code}</div>
                    <div style="font-size: 13px; color: #6c757d;">Expires in 5 minutes</div>
                </div>
                
                <div class="instructions">
                    <p><strong>How to use this code:</strong></p>
                    <ol>
                        <li>Go back to your Smart Cane Guardian app</li>
                        <li>Enter the 6-digit code shown above</li>
                        <li>Click "Verify" to complete the process</li>
                    </ol>
                </div>
                
                <div class="warning-box">
                    <div class="warning-title">
                        Important Security Notice
                    </div>
                    <p class="warning-text">
                        • Never share this code with anyone<br>
                        • If you didn't request this change, please secure your account<br>
                        • This code will expire in 5 minutes for security reasons
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" class="button">Go to Verification Page</a>
                </p>
            </div>
            
            <div class="footer">
                <div class="logo">Smart Cane</div>
                <p>Enhancing mobility and safety for visually impaired individuals</p>
                
                <div class="support-info">
                    <p>Need help? Contact our support team at iCane2026@gmail.com</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                    <p>© 2024 Smart Cane. All rights reserved.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_body = f"""
    Smart Cane Guardian - Email Verification
    
    Hello {guardian_name},
    
    You have requested to {action_text} for your Smart Cane Guardian account.
    To complete this request, please use the verification code below:
    
    Verification Code: {otp_code}
    
    This code will expire in 5 minutes.
    
    How to use this code:
    1. Go back to your Smart Cane Guardian app
    2. Enter the 6-digit code shown above
    3. Click "Verify" to complete the process
    
     Important Security Notice:
    • Never share this code with anyone
    • If you didn't request this change, please secure your account
    • This code will expire in 5 minutes.
    
    Need help? Contact our support team at support@smartcane.com
    
    This is an automated message, please do not reply to this email.
    
    © 2026 Smart Cane. All rights reserved.
    """
    
    return subject, html_body, text_body