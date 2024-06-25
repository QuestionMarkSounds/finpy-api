import stripe
import os
from flask import jsonify
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library
load_dotenv(find_dotenv())

def session_request(domain_url, price, email):
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
    return {"redirect": checkout_session.url, "sessionId": checkout_session.id, "customerId": checkout_session.customer}

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

def delete_customer_request(customer_id):
    delete_request = stripe.Customer.delete(customer_id)
    return delete_request.deleted



