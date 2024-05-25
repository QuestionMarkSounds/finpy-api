# This example sets up an endpoint using the Flask framework.
# To learn more about Flask, watch this video: https://youtu.be/7Ul1vfsmsDck.
from http import HTTPStatus
import traceback
import stripe
import json
import os


from flask import Blueprint, Flask, render_template, jsonify, request, send_from_directory, redirect
from dotenv import load_dotenv, find_dotenv

stripe.api_key = 'sk_test_51PIaYt02koWkZWym0UaKD23cT7DFdp9ZX37ifRTGALZXYZF2E2rvqreQHjqt0hU6912scvr5D8t0XUwT3FPCoKFj00sMz030XV'
# stripe_routes = Blueprint('simple_page', __name__, template_folder='templates')




# Setup Stripe python client library
load_dotenv(find_dotenv())
# For sample support and debugging, not required for production:
# stripe.set_app_info(
#     'stripe-samples/checkout-single-subscription',
#     version='0.0.1',
#     url='https://github.com/stripe-samples/checkout-single-subscription')

# # stripe.api_version = '2020-08-27'
# stripe.api_key = os.getenv('STRIPE_SECRET_KEY')



# # @stripe_routes.route('/', methods=['GET'])
# # def get_example():
# #     return render_template('index.html')


# @stripe_routes.route('/pconfig', methods=['GET'])
# def get_publishable_key():
#     return jsonify({
#         'publishableKey': os.getenv('STRIPE_PUB_KEY'),
#         'basicPrice': os.getenv('BASIC_PRICE_ID'),
#         'proPrice': os.getenv('PREMIUM_PRICE_ID')
#     })


# # Fetch the Checkout Session to display the JSON result on the success page
# @stripe_routes.route('/checkout-session', methods=['GET'])
# def get_checkout_session():
#     id = request.args.get('sessionId')
#     checkout_session = stripe.checkout.Session.retrieve(id)
#     return jsonify(checkout_session)


# @stripe_routes.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     data = request.json
#     email = data.get('email')
#     price = data.get('priceId')
#     domain_url = data.get('redirectUri')
#     user_intent = data.get('userIntent')
#     try:
#         session_id_response = get_stripe_session(email)
#         if "sessionId" not in  session_id_response.keys():
#             raise Exception(session_id_response['message'])
#         else:
#             if user_intent == "portal":
#                 customer_portal(session_id_response["sessionId"])
#             elif user_intent == "subscription":
#                 final_response = session_request(session_id_response["sessionId"], domain_url, price)
#                 if "sessionId" in final_response.keys():
#                     set_stripe_session(email, final_response["sessionId"])
#                     del final_response['sessionId']
#                 return jsonify(final_response), 303 
#             else:
#                 raise Exception("Invalid user intent")
        
#     except Exception as e:
#         print(e)
#         print(traceback.format_exc())
#         return jsonify({'error': {'message': str(e)}}), 400

def session_request(session_id, domain_url, price, email):
    # if session_id is not None:
    if False:
        checkout_session_id = session_id
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        return_url = domain_url
        session = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        return {"redirect": session.url}        
        return jsonify({"redirect": session.url}), 303 
    else:
        checkout_session = stripe.checkout.Session.create(
            
            success_url=domain_url + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/canceled',
            mode='subscription',
            customer_email = email,
            # automatic_tax={'enabled': True},
            line_items=[{
                'price': price,
                'quantity': 1,
            }],

        )
        return {"redirect": checkout_session.url, "sessionId": checkout_session.id}
        return jsonify({"redirect": checkout_session.url}), 303 

def customer_portal(customer_id):
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = os.getenv("DOMAIN")

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return jsonify({"redirect": session.url}), 303 


# @stripe_routes.route('/webhook', methods=['POST'])
# def webhook_received():
#     # You can use webhooks to receive information about asynchronous payment events.
#     # For more about our webhook events check out https://stripe.com/docs/webhooks.
#     webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
#     request_data = json.loads(request.data)

#     if webhook_secret:
#         # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
#         signature = request.headers.get('stripe-signature')
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload=request.data, sig_header=signature, secret=webhook_secret)
#             data = event['data']
#         except Exception as e:
#             return e
#         # Get the type of webhook event sent - used to check the status of PaymentIntents.
#         event_type = event['type']
#     else:
#         data = request_data['data']
#         event_type = request_data['type']
#     data_object = data['object']

#     print('event ' + event_type)

#     if event_type == 'checkout.session.completed':
#         print('🔔 Payment succeeded!')

#     return jsonify({'status': 'success'})




