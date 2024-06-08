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





