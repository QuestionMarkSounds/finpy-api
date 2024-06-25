

from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import decode_session_token, generate_session_token
from utils.jwt_utils import validate_request_with_token

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/user', methods=['POST'])
def load_user_data():

    connection = current_app.config['connection']
    config = current_app.config['config']

    data = request.json
    email = data.get('email')
    session_token = data.get('sessionToken')
    try:
        token_payload = validate_request_with_token(session_token, email, config)
    except Exception as e:
        return jsonify({'message': str(e)}), 403
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (token_payload["email"],))
        result = cursor.fetchone()
        del result["password"]
        token = generate_session_token(result, config)
        result["token"] = token
        return jsonify({'user': result}), 201
    except Exception as error:
        print('Error [Load Data]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()