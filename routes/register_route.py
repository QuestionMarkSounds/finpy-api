

from http import HTTPStatus
import os
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import generate_session_token


registration_bp = Blueprint('registration', __name__, template_folder='templates')

@registration_bp.route('/api/registration', methods=['POST'])
def registration():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        token = data.get('token')
        name = data.get('name')
        email = data.get('email')
        if email != recruiterVerification(token, config):
            return jsonify({'message': 'Invalid token'}), 403
        password = data.get('password') + os.environ.get("ROACH_KING")
        password_hash = generate_password_hash(password)
        if not email or not name or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET name = %s, password = %s WHERE email = %s RETURNING *", (name, password_hash, email))
        
        connection.commit()
        result = cursor.fetchone()
        del result['password']
        token = generate_session_token(result, config)
        result["token"] = token
        return jsonify({'result': result}), 201
    except Exception as error:
        print('Error [Registration]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()