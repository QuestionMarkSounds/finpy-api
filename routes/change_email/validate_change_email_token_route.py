

import datetime
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import decodeChangeEmailToken, recruiterVerification

validate_change_email_token_bp = Blueprint('validate_change_email_token', __name__, template_folder='templates')

@validate_change_email_token_bp.route('/validate-change-email-token', methods=['POST'])
def validate_change_email_token():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        token = data.get('token')
        if not token:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_dumpster WHERE data = %s"	, (token,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            old_email, new_email, exp = decodeChangeEmailToken(token, config)
            if datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(exp):
                return jsonify({'message': 'Token expired'}), 403
            else:
                cursor.execute("UPDATE flutter_users SET email = %s WHERE email = %s"	, (new_email, old_email))
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error [JWT]:', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()