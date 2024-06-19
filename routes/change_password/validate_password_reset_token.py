import datetime
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import decodeResetToken, recruiterVerification

validate_password_reset_token_bp = Blueprint('validate_password_reset_token', __name__, template_folder='templates')

@validate_password_reset_token_bp.route('/validate-password-reset-token', methods=['POST'])
def validate_password_reset_token():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        token = data.get('token')
        print("Token: ", token, "Length: ", len(token))
        if not token:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_dumpster WHERE data = %s"	, (token,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            email, exp = decodeResetToken(token, config)
            if datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(exp):
                return jsonify({'message': 'Token expired'}), 403
            else:
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': str(error)}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()