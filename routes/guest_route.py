
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruitRoaches, recruiterVerification

guest_bp = Blueprint('guest', __name__, template_folder='templates')


@guest_bp.route('/guest', methods=['POST'])
def unverified_guest():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        email = data.get('email')
        print("Email: ", email)
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("INSERT INTO flutter_users (email) VALUES (%s)", (email,))
        connection.commit()
        recruitRoaches(email, config)
        return jsonify({'result': "ok"}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        if ("duplicate key value" in str(error) and "Key (email)" in str(error)):
            connection.rollback()
            cursor.execute("SELECT verified FROM flutter_users WHERE email = %s", (email,))
            
            response = cursor.fetchone()
            print(response)

            if response["verified"] == False:
                recruitRoaches(email, config)
                return jsonify({'result': "ok"}), 201
            else:
                return jsonify({'message': 'User already registered'}), 500
        

        else:
            return jsonify({'message': 'Internal server error'}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()