

from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification
from utils.jwt_utils import decode_session_token, generate_session_token
from utils.jwt_utils import validate_request_with_token

change_name_bp = Blueprint('change_name', __name__, template_folder='templates')

@change_name_bp.route('/change-name', methods=['POST'])
def change_name():
    try:
        connection = current_app.config['connection']
        config = current_app.config['config']
    except TypeError as e:
        print(f"fill: {current_app.config}, exception: {str(e)}")
    data = request.json
    email = data.get('email')
    name = data.get('newName')
    session_token = data.get('sessionToken')
    try:
        token_payload = validate_request_with_token(session_token, email, config)
    except Exception as e:
        return jsonify({'message': str(e)}), 403
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE public.flutter_users set name = %s WHERE email = %s RETURNING *", (name, token_payload["email"],))
        result = cursor.fetchone()
        del result["password"]
        token = generate_session_token(result, config)
        result["token"] = token
        print("USER INFO: ",result)
        stripe.Customer.modify(result["customer_id"], metadata = {"name":name})
        return jsonify({'user': result}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()