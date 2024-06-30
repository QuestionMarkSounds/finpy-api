

from http import HTTPStatus
import os
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import decode_session_token, generate_session_token
from utils.jwt_utils import validate_request_with_token
from routes.stripe.stripe_server import delete_customer_request

delete_account_bp = Blueprint('delete_account', __name__, template_folder='templates')

@delete_account_bp.route('/api/delete-account', methods=['POST'])
def delete_account():

    connection = current_app.config['connection']
    config = current_app.config['config']

    data = request.json
    email = data.get('email')
    password = data.get('password')
    session_token = data.get('sessionToken')
    try:
        token_payload = validate_request_with_token(session_token, email, config)
    except Exception as e:
        return jsonify({'message': str(e)}), 403
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (token_payload["email"],))
        result = cursor.fetchone()
        if result:
            password_hash = result["password"] 
            if check_password_hash(password_hash, password+os.environ.get("ROACH_KING")):
                cursor.execute("DELETE FROM public.flutter_users WHERE email = %s RETURNING *", (token_payload["email"],))
                if result["customer_id"] != None:
                    delete_customer_request(result["customer_id"])
                return jsonify({'result': 'account deleted'}), HTTPStatus.OK.value
        return jsonify({'message': 'Invalid credentials'}), 403
    except Exception as error:
        print('Error [Delete Account]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
            
            
@delete_account_bp.route('/api/delete-account-platform', methods=['POST'])
def delete_account_platform():

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
        if result:
            platform = result["platform"] 
            if platform != "none":
                cursor.execute("DELETE FROM public.flutter_users WHERE email = %s RETURNING *", (token_payload["email"],))
                if result["customer_id"] != None:
                    delete_customer_request(result["customer_id"])
                return jsonify({'result': 'account deleted'}), HTTPStatus.OK.value
        return jsonify({'message': 'Invalid credentials'}), 403
    except Exception as error:
        print('Error [Delete Account]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()