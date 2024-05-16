import smtplib
from email.mime.text import MIMEText
from dotenv import dotenv_values, load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError
from cryptography.hazmat.primitives import serialization
# read and load the key
private_key = open('.ssh/id_rsa', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

load_dotenv(".env", override=True)
config = dotenv_values(".env")
def recruiteRoaches(email, config):
    payload_data = {
        "email": email+config["ROACH_PRINCESS"]
    }
    new_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )


    print(config)
    subject = "Email Subject"
    body = "This is the body of the text message"
    sender = config["ROACH_RECRUITER"]
    recipients = ["marksdocenko@outlook.com"]
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
            key='my_super_secret',
            algorithms=[header_data['alg'], ]
        )
    except ExpiredSignatureError as error:
        print(f'Unable to decode the token, error: {error}')