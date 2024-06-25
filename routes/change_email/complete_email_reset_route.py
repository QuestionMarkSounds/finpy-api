import datetime
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import decodeResetToken, notify_about_email_change, recruiterVerification

complete_email_reset_bp = Blueprint('complete_email_reset', __name__, template_folder='templates')


@complete_email_reset_bp.route('/complete-email-reset', methods=['POST'])
def complete_email_reset():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        token = data.get('token')
        new_email = data.get('email')
        if not token or not new_email:
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
                cursor.execute("UPDATE flutter_users SET  email = %s WHERE email = %s RETURNING *", (new_email, email))
                
                result = cursor.fetchone()
                notify_about_email_change(email, new_email, response["name"], config)
                stripe.Customer.modify(result["customer_id"], metadata = {"email":new_email})
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error [Complete Email Reset]:', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()