import datetime
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import dotenv_values, load_dotenv
import jwt
from cryptography.hazmat.primitives import serialization
# read and load the key

 
load_dotenv(".env", override=True)
config = dotenv_values(".env")

private_key = os.environ.get("JWT_SSH_KEY")
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')


def recruitRoaches(email, config):
    payload_data = {
        "email": email+os.environ.get("ROACH_PRINCESS")
    }
    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )

    subject = "Verify your email address"
    body = "Please click on the following link to verify your email address: {}/verifyEmail?token=".format(os.environ.get("CLIENT_URL"))+new_token
    sender = os.environ.get("ROACH_RECRUITER")
    recipients = [email]
    password = os.environ.get("ROACH_CRY")

    send_email(subject, body, sender, recipients, password)

def contactUsEmail(email, name, message, config):
    subject = "Contact Us: {}".format(email)
    body = "Contact Us Request: \n\nName: {}\nEmail: {}\n\nMessage: {}".format(name, email, message)
    sender = os.environ.get("ROACH_RECRUITER")
    recipients = [sender]
    password = os.environ.get("ROACH_CRY")

    send_email(subject, body, sender, recipients, password)

def resetLink(email, name, reason, config):
    payload_data = {
        "email": email+os.environ.get("ROACH_PRINCESS"),
        "reason": reason,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
    }
    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )

    subject = "Fintelligence Password reset"
    body = f"Hi {name}! Please click on the following link to reset your password: http://localhost:63621/resetPassword?token="+new_token
    sender = os.environ.get("ROACH_RECRUITER")
    recipients = [email]
    password = os.environ.get("ROACH_CRY")

    send_email(subject, body, sender, recipients, password)
    return new_token

def changeEmailLink(old_email, new_email, name, reason, config):
    payload_data = {
        "email": old_email+os.environ.get("ROACH_PRINCESS"),
        "new_email": new_email+os.environ.get("ROACH_PRINCESS"),
        "reason": reason,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
    }
    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )

    subject = "Fintelligence Email reset"
    body = f"Hi {name}! Please click on the following link to change your email adress: http://localhost:63621/changeEmail?token="+new_token
    sender = os.environ.get("ROACH_RECRUITER")
    recipients = [new_email]
    password = os.environ.get("ROACH_CRY")

    send_email(subject, body, sender, recipients, password)
    return new_token

def notify_about_email_change(email, new_email, name, config):
    subject = "Fintelligence Email change"
    body = f"Hi {name}! Your email has changed. You can now log in with your new email: {new_email}"
    sender = os.environ.get("ROACH_RECRUITER")
    recipients = [email]
    password = os.environ.get("ROACH_CRY")

    send_email(subject, body, sender, recipients, password)


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())

def recruiterVerification(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        return payload["email"].replace(os.environ.get("ROACH_PRINCESS"), "")
    except Exception as error:
        print(f'Unable to decode the token, error: {error}')

def decodeResetToken(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        
        return payload["email"].replace(os.environ.get("ROACH_PRINCESS"), ""), payload["exp"]
    except Exception as error:
        print(f'Unable to decode the token, error: {error}')

def decodeChangeEmailToken(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        
        return payload["email"].replace(os.environ.get("ROACH_PRINCESS"), ""), payload["new_email"].replace(os.environ.get("ROACH_PRINCESS"), ""), payload["exp"]
    except Exception as error:
        print(f'Unable to decode the token, error: {error}')
