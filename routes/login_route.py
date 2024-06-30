

from http import HTTPStatus
import os
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from utils.jwt_utils import generate_session_token

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/api/login', methods=['POST'])
def login():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * from flutter_users WHERE email = %s", (email,))
        connection.commit()
        result = cursor.fetchone()
        if result:
            
            if result["platform"] != "none":
                return jsonify({'message': 'User registered using different authentication method'}), 403
            password_hash = result["password"] 

            if check_password_hash(password_hash, password+os.environ.get("ROACH_KING")):
                reply = result
                del reply["password"]
                token =generate_session_token(reply, config)
                reply["token"] = token
                return jsonify({'result': reply}), HTTPStatus.OK.value
            else:
                return jsonify({'message': 'Invalid credentials'}), 403
        else:
            return jsonify({'message': 'Not a registered user'}), HTTPStatus.NOT_FOUND.value
    except Exception as error:
        print('Error [Login]:', error)
        print(traceback.format_exc())
        return jsonify({'message': str(error)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()