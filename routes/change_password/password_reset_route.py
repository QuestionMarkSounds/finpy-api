from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruiterVerification, resetLink

password_reset_bp = Blueprint('password_reset', __name__, template_folder='templates')

@password_reset_bp.route('/password-reset', methods=['POST'])
def password_reset():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        email = data.get('email')
        print("Email: ", email)
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_users WHERE email = %s"	, (email,))
        connection.commit()
        response = cursor.fetchone()
        print(response)
        if (response):
            token = resetLink(email, response["name"], "resetLink", config)
            cursor.execute("INSERT INTO flutter_dumpster (data) VALUES (%s)", (token,))

            connection.commit()
            print("Token in: ", token)
            return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'User not found'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()