

from http import HTTPStatus
import json
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from stripe_utils import get_product_from_subscription, Subscription
from routes.stripe.stripe_customer import get_stripe_customer, set_stripe_subscription
from routes.stripe.stripe_server import customer_portal, session_request
from utils.jwt_utils import validate_request_with_token

stripe_ccs_bp = Blueprint('stripe_create_checkout_session', __name__, template_folder='templates')

@stripe_ccs_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    connection = current_app.config['connection']
    config = current_app.config['config']

    data = request.json
    email = data.get('email')
    price = data.get('priceId')
    domain_url = data.get('redirectUri')
    user_intent = data.get('userIntent')
    session_token = data.get('sessionToken')

    try:
        validate_request_with_token(session_token, email, config)
    except Exception as e:
        return jsonify({'message': str(e)}), 403

    try:
        customer_id_response = get_stripe_customer(email, connection)
        print(customer_id_response)
        if "customerId" not in  customer_id_response.keys():
            raise Exception(customer_id_response['message'])
        else:
            if user_intent == "portal":
                customer_portal(customer_id_response["sessionId"])
            elif user_intent == "subscription":
                print("----sID-----")
                print(customer_id_response["customerId"])
                final_response = session_request(None, domain_url, price, email)
                print(final_response)
                if "sessionId" in final_response.keys():
                    del final_response['sessionId']
                
                return jsonify(final_response), 303 
            else:
                raise Exception("Invalid user intent")
        
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': {'message': str(e)}}), 400
    
@stripe_ccs_bp.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)

