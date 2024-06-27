from http import HTTPStatus
import traceback
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import changeEmailLink, recruiterVerification
from utils.jwt_utils import validate_request_with_token

change_email_bp = Blueprint('change_email', __name__, template_folder='templates')


@change_email_bp.route('/change-email', methods=['POST'])
def change_email():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        old_email = data.get('email')
        new_email = data.get('new_email')
        password = data.get('password')
        session_token = data.get('sessionToken')
        # 
        try:
            token_payload = validate_request_with_token(session_token, old_email, config)
        except Exception as e:
            return jsonify({'message': str(e)}), 403
        
        
        if not old_email or not new_email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_users WHERE email = %s"	, (new_email,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            return jsonify({'message': 'New email already in use'}), 403
        cursor.execute("SELECT * FROM flutter_users WHERE email = %s"	, (old_email,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            password_hash = response["password"] 

            if not check_password_hash(password_hash, password+os.environ.get("ROACH_KING")):
                return jsonify({'message': 'Invalid credentials'}), 403

            token = changeEmailLink(old_email, new_email, response["name"], "changeEmail", config)
            cursor.execute("INSERT INTO flutter_dumpster (data) VALUES (%s)", (token,))
            connection.commit()
            
            return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'User not found'}), 403
    except Exception as error:
        print('Error [Change Email]:', error)
        return jsonify({'message': str(error)}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()