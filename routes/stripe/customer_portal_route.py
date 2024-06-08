from http import HTTPStatus
import json
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from stripe_utils import get_product_from_subscription, Subscription
from routes.stripe.stripe_customer import set_stripe_subscription, get_stripe_customer
from utils.jwt_utils import validate_request_with_token

stripe_customer_portal_bp = Blueprint('stripe_customer_portal', __name__, template_folder='templates')


@stripe_customer_portal_bp.route('/customer-portal', methods=['POST'])
def get_customer_portal():
    connection = current_app.config['connection']
    config = current_app.config['config']
    try:
        data = request.json
        email = data.get('email')
        session_token = data.get('sessionToken')

        try:
            validate_request_with_token(session_token, email, config)
        except Exception as e:
            print("Token error: ", e)
            return jsonify({'message': str(e)}), 403

        return_url = data.get('returnUrl')
        customer_id = get_stripe_customer(email, connection)
        checkout_session = stripe.billing_portal.Session.create(
            customer = customer_id["customerId"],
            return_url = return_url

        )
        return jsonify({"redirect": checkout_session.url}), 201
    
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': {'message': str(e)}}), 400