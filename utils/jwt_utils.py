import datetime
import os
import jwt
from cryptography.hazmat.primitives import serialization
from flask import current_app
from roach_recruitment import key

def generate_session_token(user_info, config):
    user = dict(user_info)
    # payload_data = dict(user_info)
    payload_data = {
        "id": user["id"],
        # "created_at": user["created_at"],
        "email": user["email"] + os.environ.get("ROACH_PRINCESS"),
        "subscription_type": user["subscription_type"],
        "verified": user["verified"],
        "name": user["name"],
        "platform": user["platform"],
        "stripe_session": user["stripe_session"],
        "customer_id": user["customer_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14) 
    }
    session_token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )

    return session_token

def decode_session_token(token, config):
    header_data = jwt.get_unverified_header(token)
    try:
        payload = jwt.decode(
            token,
            key=key.public_key(),
            algorithms=[header_data['alg'], ]
        )
        
        payload["email"].replace(os.environ.get("ROACH_PRINCESS"), "")
        return payload
    except jwt.ExpiredSignatureError as error:
        raise Exception("Token expired")
    

def validate_request_with_token(token, email, config):
    payload = decode_session_token(token, config)
    payload["email"] = payload["email"].replace(os.environ.get("ROACH_PRINCESS"), "")
    if email != payload["email"]:
        raise Exception("Invalid token")
    
    return payload
        
