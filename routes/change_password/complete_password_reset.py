import datetime
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import decodeResetToken, recruiterVerification

complete_password_reset_bp = Blueprint('complete_password_reset', __name__, template_folder='templates')


@complete_password_reset_bp.route('/complete-password-reset', methods=['POST'])
def complete_password_reset():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        token = data.get('token')
        password = data.get('password') + config["ROACH_KING"]
        password_hash = generate_password_hash(password)
        if not token or not password:
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
                cursor.execute("UPDATE flutter_users SET  password = %s WHERE email = %s RETURNING *", (password_hash, email))
                cursor.execute("DELETE FROM flutter_dumpster WHERE data = %s"	, (token,))
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error [Complete Password Reset]:', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()