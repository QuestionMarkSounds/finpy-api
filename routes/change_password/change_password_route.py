

from http import HTTPStatus
import traceback
from flask import Blueprint, current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import validate_request_with_token

change_password_bp = Blueprint('change_password', __name__, template_folder='templates')

@change_password_bp.route('/change-password', methods=['POST'])
def change_password():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        new_password = data.get('newPassword')
        old_password = data.get('oldPassword')
        email = data.get('email')
        session_token = data.get('sessionToken')

        try:
            validate_request_with_token(session_token, email, config)
        except Exception as e:
            return jsonify({'message': str(e)}), 403

        if not email or not new_password or not old_password :
            return jsonify({'message': 'Invalid input'}), HTTPStatus.BAD_REQUEST.value
        cursor = connection.cursor()
        cursor.execute("SELECT * from flutter_users WHERE email = %s", (email,))
        connection.commit()
        result = cursor.fetchone()
        if result:
            
            password_hash = result["password"] 

            if check_password_hash(password_hash, old_password+config["ROACH_KING"]):
                pass
                
            else:
                return jsonify({'message': 'Invalid credentials'}), HTTPStatus.FORBIDDEN.value
        else:
            return jsonify({'message': 'Not a registered user'}), HTTPStatus.NOT_FOUND.value

        password = data.get('new_password') + config["ROACH_KING"]
        password_hash = generate_password_hash(password)

        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SETpassword = %s WHERE email = %s RETURNING *", (password_hash, email))
        
        connection.commit()
        result = cursor.fetchone()
        del result['password']
        return jsonify({'result': result}), HTTPStatus.OK.value
    except Exception as error:
        print('Error [Change Password]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()