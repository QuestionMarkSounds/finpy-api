

from http import HTTPStatus
import json
import traceback
from flask import Blueprint, jsonify, request, current_app
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from stripe_utils import get_product_from_subscription, Subscription
from routes.stripe.stripe_customer import set_stripe_subscription

stripe_webhook_bp = Blueprint('stripe_webhook', __name__, template_folder='templates')

@stripe_webhook_bp.route('/webhook', methods=['POST'])
def webhook_received():

    connection = current_app.config['connection']
    config = current_app.config['config']
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = config['STRIPE_WEBHOOK_SECRET']
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']
    
    # print('WH event ' + event_type)
    if event_type == 'customer.subscription.updated':
        json_subscription = stripe.Subscription.list(customer = data_object['customer'])
        product_id = get_product_from_subscription(json_subscription)
        subscription_tier = Subscription.name_from_id(product_id)
        print(data_object)
        set_stripe_subscription(data_object['customer'], subscription_tier, connection)

    if event_type == 'customer.subscription.deleted':
        # json_subscription = stripe.Subscription.list(customer = data_object['customer'])
        # product_id = get_product_from_subscription(json_subscription)
        subscription_tier = "none"
        set_stripe_subscription(data_object['customer'], subscription_tier, connection)
        
    if event_type == 'checkout.session.completed':
        json_subscription = stripe.Subscription.list(customer = data_object['customer'])
        product_id = get_product_from_subscription(json_subscription)
        
        subscription_tier = Subscription.name_from_id(product_id)
        print('🔔 Payment succeeded!')
        # print(json_subscription)
        print("------------------")
        set_stripe_subscription(data_object['customer_email'], data_object['customer'], subscription_tier, connection)
        # print(request_data)
        print("------------------")
        # print(data)

    return jsonify({'status': 'success'}), 200