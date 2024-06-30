

from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification

jwt_verification_bp = Blueprint('jwt_verification', __name__, template_folder='templates')


@jwt_verification_bp.route('/api/verification', methods=['POST'])
def jwt_verification():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        jwt = data.get('token')
        email = recruiterVerification(jwt, config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (email,))
        response = cursor.fetchall()

        if response[0]["verified"] == "true":
            return jsonify({'message': 'User already verified'}), 409
        else:
            cursor.execute("UPDATE public.flutter_users SET verified = 'true' WHERE email = %s", (email,))
            return jsonify({'message': 'Accepted'}), 202
    except Exception as error:
        print('Error [JWT]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()