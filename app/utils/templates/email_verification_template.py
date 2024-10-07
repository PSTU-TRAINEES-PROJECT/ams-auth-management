VERIFICATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: white;
            margin: 0;
            padding: 0;
        }
        .email-container {
            max-width: 600px;
            margin: 20px auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            padding: 20px;
        }
        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #dddddd;
        }
        .header h1 {
            color: #333333;
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 20px;
            color: #555555;
            line-height: 1.6;
            text-align: left;
        }
        .button-container {
            text-align: center;
            padding: 20px 0;
        }
        .verify-button {
            background-color: White;   /* Button color black */
            color: black;            /* Text color white */
            padding: 12px 24px;
            font-size: 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s; /* Smooth transition for hover effect */
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #777777;
            margin-top: 20px;
            border-top: 1px solid #dddddd;
            padding-top: 20px;
        }
        .footer a {
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Email Verification</h1>
        </div>
        <div class="content">
            <p>Hi {{user_name}},</p>
            <p>Thank you for registering with AMS! To complete your registration, please verify your email address by clicking the button below.</p>
            <div class="button-container">
                <a href="{{verification_url}}" class="verify-button">Verify Email</a>
            </div>
            <p>If you did not create an account, you can safely ignore this email. If you have any questions, feel free to contact our support team.</p>
            <p>Best Regards,<br>The AMS Team</p>
        </div>
        <div class="footer">
            <p>Need help? <a href="mailto:support@ams.com">Contact Support</a></p>
            <p>&copy; 2024 AMS, Inc. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
