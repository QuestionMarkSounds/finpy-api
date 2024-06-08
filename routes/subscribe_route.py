

from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification

subscribe_bp = Blueprint('subscribe', __name__, template_folder='templates')

@subscribe_bp.route('/subscribe', methods=['POST'])
def subscribe():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        email = data.get('email')
        subscription_type = data.get('subscription_type')
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET subscription_type = %s WHERE email = %s", (subscription_type, email))
        
        connection.commit()
        # result = cursor.fetchone()
        return jsonify({'result': 'ok'}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()