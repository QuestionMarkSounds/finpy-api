from http import HTTPStatus
import requests
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import decode_session_token, generate_session_token
from utils.jwt_utils import validate_request_with_token

google_auth_bp = Blueprint('google_auth', __name__, template_folder='templates')

@google_auth_bp.route('/api/google-auth', methods=['POST'])
def google_auth():

    connection = current_app.config['connection']
    config = current_app.config['config']

    data = request.json
    access_token_type = data.get('accessTokenType')
    access_token_data = data.get('accessTokenData')
    access_token_expiry = data.get('accessTokenExpiry')
    try:
        verify_google_access_token_response = verify_google_access_token(access_token_type, access_token_data, access_token_expiry)
    except Exception as e:
        return jsonify({'message': str(e)}), 403
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from public.flutter_users WHERE email = %s", (verify_google_access_token_response["email"],))
        result = cursor.fetchone()
        
        if (result == None):
            cursor.execute("INSERT INTO public.flutter_users (email, platform, verified, name) VALUES (%s, 'google', %s, %s) RETURNING *", (verify_google_access_token_response["email"],verify_google_access_token_response["verified_email"],verify_google_access_token_response["name"],))   
            result = cursor.fetchone()
            
        else:
            if result["platform"] != "google":
               return jsonify({'message': 'User registered using different authentication method'}), 403 
        
        del result["password"]
        token = generate_session_token(result, config)
        result["token"] = token
        return jsonify({'result': result}), 201
    except Exception as error:
        print('Error [Google Auth]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()


def verify_google_access_token(tokenType, tokenData, tokenExpiry):
    url = "https://www.googleapis.com/userinfo/v2/me"
    headers = {'Content-length': '0',
                'Authorization': '{} {}'.format(tokenType, tokenData),
            }
    response = requests.get(url, headers=headers)
    return response.json()
