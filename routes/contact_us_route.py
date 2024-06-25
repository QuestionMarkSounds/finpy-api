
from http import HTTPStatus
import traceback
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from roach_recruitment import recruitRoaches, recruiterVerification, contactUsEmail

contact_us_bp = Blueprint('contact_us', __name__, template_folder='templates')


@contact_us_bp.route('/contact-us', methods=['POST'])
def contact_us():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        if not email or not name or not message:
            return jsonify({'message': 'Invalid input data'}), 400
        contactUsEmail(email, name, message, config)
        return jsonify({'result': "ok"}), 201
    except Exception as error:
        print('Error [Contact Us]:', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
        