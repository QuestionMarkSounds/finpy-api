import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import dotenv_values, load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError
from cryptography.hazmat.primitives import serialization
# read and load the key
private_key = open('ssh/.ssh/id_rsa', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

load_dotenv(".env", override=True)
config = dotenv_values(".env")
def recruitRoaches(email, config):
    payload_data = {
        "email": email+config["ROACH_PRINCESS"]
    }
    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )

    subject = "Verify your email address"
    body = "Please click on the following link to verify your email address: http://localhost:63621/verifyEmail?token="+new_token
    sender = config["ROACH_RECRUITER"]
    recipients = [email]
    password = config["ROACH_CRY"]

    send_email(subject, body, sender, recipients, password)


def resetLink(email, name, reason, config):
    payload_data = {
        "email": email+config["ROACH_PRINCESS"],
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
    sender = config["ROACH_RECRUITER"]
    recipients = [email]
    password = config["ROACH_CRY"]

    send_email(subject, body, sender, recipients, password)
    return new_token

def changeEmailLink(email, name, reason, config):
    payload_data = {
        "email": email+config["ROACH_PRINCESS"],
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
    sender = config["ROACH_RECRUITER"]
    recipients = [email]
    password = config["ROACH_CRY"]

    send_email(subject, body, sender, recipients, password)
    return new_token

def notify_about_email_change(email, new_email, name, config):
    subject = "Fintelligence Email change"
    body = f"Hi {name}! Your email has changed. You can now log in with your new email: {new_email}"
    sender = config["ROACH_RECRUITER"]
    recipients = [email]
    password = config["ROACH_CRY"]

    send_email(subject, body, sender, recipients, password)


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def recruiterVerification(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        print("Payload: ", payload)
        return payload["email"].replace(config["ROACH_PRINCESS"], "")
    except ExpiredSignatureError as error:
        print(f'Unable to decode the token, error: {error}')

def decodeResetToken(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        print("Payload: ", payload)
        return payload["email"].replace(config["ROACH_PRINCESS"], ""), payload["exp"]
    except ExpiredSignatureError as error:
        print(f'Unable to decode the token, error: {error}')

