PASSWORD_RESET_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">

    <style>
        body{
            font-family: Montserrat, serif;
            margin: 0;
            padding: 0;
        }
        .email-container{
            padding: 2rem;
        }
        .email-container-inner{
            text-align: center;
            padding: 2rem 3rem 2rem 3rem;
            border-radius: 1rem; 
            box-shadow: 0 0 12px 8px #ACA0A040;
            max-width: 20rem;
            margin: 0 auto;
        }
        .email-container-inner-imgDiv{
            text-align: center;
            margin: 0 auto;
        }
        .email-container-inner-imgDiv img{
            width: 60px;
            height: 60px;
            display: inline-block;
            margin: 0 auto;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        .bouncy {
            animation: bounce 2s infinite;
        }
        .email-container-inner-textDiv h3{
            font-size: 1.5rem;
            color: #3498DB; 
            font-weight: 500;
        }
        .email-container-inner-textDiv p{
            color: #595959; 
            font-size: 0.8rem;
        }
        .email-container-inner-textDiv span{
            color: #000;
            font-weight: bold;
        }
        .btn{
            width: auto; 
            border: none; 
            outline: none; 
            cursor: pointer;
            padding: 0.6rem 1.5rem 0.6rem 1.5rem; 
            background-color: #3498DB; 
            color: #fff; 
            border-radius: 0.5rem; 
            font-size: 0.8rem; 
            font-weight: bold;
            margin-top: 0.5rem;
        }
        .btn:hover
        {
            background-color: #268bcf;
        }
    </style>

</head>
<body>
    <div class="email-container">
        <div class="email-container-inner">
          <div class="email-container-inner-imgDiv">
            <img src="https://i.ibb.co.com/yXqHRnG/email.png" alt="envelope icon" class="bouncy" style="display: inline-block; margin: 0 auto;">
          </div>
           <div class="email-container-inner-textDiv">
               <h3>Hi {{user_name}},</h3>
               <p>We received a request to reset your password.
               <br/>This link will expire in 15 minutes. Click the button below to reset it</p>
           </div>
           <a href="{{reset_url}}" style="text-decoration: none;">
            <button class="btn">Reset Password</button>
            </a>
            <div class="email-container-inner-textDiv">
                <p>If you did not request a password reset, please ignore this email.</p>
            </div>
        </div>
     </div>
</body>
</html>
"""
