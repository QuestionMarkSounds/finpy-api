import datetime
import json
import os
from flask import Blueprint, Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import atexit
import traceback
import stripe
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import dotenv_values

from apscheduler.schedulers.background import BackgroundScheduler

from roach_recruitment import changeEmailLink, decodeChangeEmailToken, decodeResetToken, notify_about_email_change, recruiterVerification, recruitRoaches, resetLink, send_email
from http import HTTPStatus
from stripe_server import session_request, customer_portal
from stripe_utils import get_product_from_subscription, Subscription

config = dotenv_values(".env")

def get_db_connection():
    try:
        
        connection = psycopg2.connect(
            dbname=os.environ.get("INFESTATION_PROPAGATOR"), 
            user=os.environ.get("INFESTATION_TARGET"),
            password=os.environ.get("INFESTATION_KEY"), 
            host=os.environ.get("INFESTATION_HOST"),
            port=os.environ.get("INFESTANT_AMOUNT"),
            cursor_factory=RealDictCursor
        )
        print('Successful connection to the database')
        return connection
        
    except Exception as error:
        print('Database connection error:', str(error))

connection = get_db_connection()

app = Flask(__name__)

app.config['connection'] = connection
app.config['config'] = config

from routes.login_route import login_bp
app.register_blueprint(login_bp, connection = connection, config = config)

from routes.register_route import registration_bp
app.register_blueprint(registration_bp, connection = connection, config = config)

from routes.subscribe_route import subscribe_bp
app.register_blueprint(subscribe_bp, connection = connection, config = config)

from routes.load_user_route import user_bp
app.register_blueprint(user_bp, connection = connection, config = config)

from routes.jwt_verification_route import jwt_verification_bp
app.register_blueprint(jwt_verification_bp, connection = connection, config = config)

from routes.guest_route import guest_bp
app.register_blueprint(guest_bp, connection = connection, config = config)

from routes.change_name_route import change_name_bp
app.register_blueprint(change_name_bp, connection = connection, config = config)

# CHANGE PASSWORD

from routes.change_password.change_password_route import change_password_bp
app.register_blueprint(change_password_bp, connection = connection, config = config)

from routes.change_password.password_reset_route import password_reset_bp
app.register_blueprint(password_reset_bp, connection = connection, config = config)

from routes.change_password.validate_password_reset_token import validate_password_reset_token_bp
app.register_blueprint(validate_password_reset_token_bp, connection = connection, config = config)

from routes.change_password.complete_password_reset import complete_password_reset_bp
app.register_blueprint(complete_password_reset_bp, connection = connection, config = config)

# CHANGE EMAIL

from routes.change_email.change_email_route import change_email_bp
app.register_blueprint(change_email_bp, connection = connection, config = config)

from routes.change_email.validate_change_email_token_route import validate_change_email_token_bp
app.register_blueprint(validate_change_email_token_bp, connection = connection, config = config)

from routes.change_email.complete_email_reset_route import complete_email_reset_bp
app.register_blueprint(complete_email_reset_bp, connection = connection, config = config)

# DELETE ACCOUNT

from routes.delete_account_route import delete_account_bp
app.register_blueprint(delete_account_bp, connection = connection, config = config)


# STRIPE ROUTES

from routes.stripe.webhook_route import stripe_webhook_bp
app.register_blueprint(stripe_webhook_bp, connection = connection, config = config)

from routes.stripe.create_checkout_session_route import stripe_ccs_bp
app.register_blueprint(stripe_ccs_bp, connection = connection, config = config)

from routes.stripe.customer_portal_route import stripe_customer_portal_bp
app.register_blueprint(stripe_customer_portal_bp, connection = connection, config = config)

# CONTACT US ROUTE

from routes.contact_us_route import contact_us_bp
app.register_blueprint(contact_us_bp, connection = connection, config = config)

# GOOGLE AUTH ROUTES

from routes.google.google_auth_route import google_auth_bp
app.register_blueprint(google_auth_bp, connection = connection, config = config)

port = 7341

# Setup Stripe python client library
# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/checkout-single-subscription',
    version='0.0.1',
    url='https://github.com/stripe-samples/checkout-single-subscription')

# stripe.api_version = '2020-08-27'
stripe.api_key = config['STRIPE_SECRET_KEY']

def delete_old_rows():
    # Connect to the database
    cur = connection.cursor()
    # Define the time threshold (one hour ago)
    threshold = datetime.datetime.now() - datetime.timedelta(hours=1)

    # Execute the deletion query
    cur.execute("DELETE FROM flutter_dumpster WHERE created_at < %s", (threshold,))

    # Commit the transaction
    connection.commit()
    # Close the cursor and connection
    cur.close()
 
scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_rows, 'interval', hours=1)  # Run every hour
scheduler.start()

@app.route('/')
def hello_world():
    return 'Hello world!'

def close_connection():
    if 'connection' in globals():
        connection.close()
        print('Connection to the database closed')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
    atexit.register(close_connection)