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

try:
    config = dotenv_values(".env")
    connection = psycopg2.connect(
        dbname=config["INFESTATION_PROPAGATOR"], 
        user=config["INFESTATION_TARGET"],
        password=config["INFESTATION_KEY"], 
        host=config["INFESTATION_HOST"],
        port=config["INFESTANT_AMOUNT"],
        cursor_factory=RealDictCursor
    )
    print('Successful connection to the database')
except Exception as error:
    print('Database connection error:', str(error))


app = Flask(__name__)
port = 7341

# @app.after_request
# def add_header(response):
#     print("B")
#     response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline';"
#     return response




# Setup Stripe python client library
# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/checkout-single-subscription',
    version='0.0.1',
    url='https://github.com/stripe-samples/checkout-single-subscription')

# stripe.api_version = '2020-08-27'
stripe.api_key = config['STRIPE_SECRET_KEY']



# @app.route('/', methods=['GET'])
# def get_example():
#     return render_template('index.html')


def delete_old_rows():
    # Connect to the database
    cur = connection.cursor()
    # Define the time threshold (one hour ago)
    threshold = datetime.datetime.now() - datetime.timedelta(hours=1)

    # Execute the deletion query
    cur.execute("DELETE FROM flutter_dumpster WHERE created_at < %s", (threshold,))

    # Commit the transaction
    connection.commit()
    print("DUMPSTER TRUCK: Deleted old rows")	
    # Close the cursor and connection
    cur.close()
 
scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_rows, 'interval', hours=1)  # Run every hour
scheduler.start()

@app.route('/pconfig', methods=['GET'])
def get_publishable_key():
    return jsonify({
        'publishableKey': config['STRIPE_PUB_KEY'],
        'basicPrice': config['BASIC_PRICE_ID'],
        'proPrice': config['PREMIUM_PRICE_ID']
    })


# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)

@app.route('/customer-portal', methods=['POST'])
def get_customer_portal():
    try:
        data = request.json
        email = data.get('email')
        return_url = data.get('returnUrl')
        customer_id = get_stripe_customer(email)
        checkout_session = stripe.billing_portal.Session.create(
            customer = customer_id["customerId"],
            return_url = return_url

        )
        return jsonify({"redirect": checkout_session.url}), 201
    
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': {'message': str(e)}}), 400


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    email = data.get('email')
    price = data.get('priceId')
    domain_url = data.get('redirectUri')
    user_intent = data.get('userIntent')
    try:
        customer_id_response = get_stripe_customer(email)
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
                    # set_stripe_customer(email, final_response["sessionId"])
                    del final_response['sessionId']
                return jsonify(final_response), 303 
            else:
                raise Exception("Invalid user intent")
        
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return jsonify({'error': {'message': str(e)}}), 400
    
@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
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
        set_stripe_subscription(data_object['customer'], subscription_tier)

    if event_type == 'customer.subscription.deleted':
        # json_subscription = stripe.Subscription.list(customer = data_object['customer'])
        # product_id = get_product_from_subscription(json_subscription)
        subscription_tier = "none"
        set_stripe_subscription(data_object['customer'], subscription_tier)
        
    if event_type == 'checkout.session.completed':
        json_subscription = stripe.Subscription.list(customer = data_object['customer'])
        product_id = get_product_from_subscription(json_subscription)
        
        subscription_tier = Subscription.name_from_id(product_id)
        print('🔔 Payment succeeded!')
        # print(json_subscription)
        print("------------------")
        set_stripe_customer(data_object['customer_email'], data_object['customer'], subscription_tier)
        # print(request_data)
        print("------------------")
        # print(data)

    return jsonify({'status': 'success'}), 200

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/infestants')
def get_infestants():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users")
        results = cursor.fetchall()
        return jsonify({'users': results})
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/user', methods=['POST'])
def load_user_data():
    data = request.json
    email = data.get('email')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (email,))
        result = cursor.fetchone()
        del result["password"]
        print(result)
        return jsonify({'user': result}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/verification', methods=['POST'])
def jwt_verification():
    try:
        data = request.json
        # print(data.get('email'))
        jwt = data.get('token')
        email = recruiterVerification(jwt, config)
        print("JWT VERIFIED EMAIL: ", email)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (email,))
        response = cursor.fetchall()
        results = jsonify({"results": response})
        print(results)
        if response[0]["verified"] == "true":
            return jsonify({'message': 'User already verified'}), 409
        else:
            cursor.execute("UPDATE public.flutter_users SET verified = 'true' WHERE email = %s", (email,))
            return jsonify({'message': 'Accepted'}), 202
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

# @app.route('/reset-password', methods=['POST'])
# def jwt_reset_password():
#     try:
#         data = request.json
#         # print(data.get('email'))
#         jwt = data.get('token')
#         email = recruiterVerification(jwt, config)
#         print("JWT VERIFIED EMAIL: ", email)
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (email,))
#         response = cursor.fetchall()
#         results = jsonify({"results": response})
#         print(results)
#         if response[0]["verified"] == "true":
#             return jsonify({'message': 'User already verified'}), 409
#         else:
#             cursor.execute("UPDATE public.flutter_users SET verified = 'true' WHERE email = %s", (email,))
#             return jsonify({'message': 'Accepted'}), 202
#     except Exception as error:
#         print('Error', error)
#         print(traceback.format_exc())
#         return jsonify({'message': 'Internal server error'}), 500
#     finally:
#         if 'cursor' in locals():
#             cursor.close()

@app.route('/guest', methods=['POST'])
def unverified_guest():
    try:
        data = request.json
        email = data.get('email')
        print("Email: ", email)
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("INSERT INTO flutter_users (email) VALUES (%s)", (email,))
        connection.commit()
        recruitRoaches(email, config)
        return jsonify({'result': "ok"}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        if ("duplicate key value" in str(error) and "Key (email)" in str(error)):
            connection.rollback()
            cursor.execute("SELECT verified FROM flutter_users WHERE email = %s", (email,))
            
            response = cursor.fetchone()
            print(response)

            if response["verified"] == False:
                recruitRoaches(email, config)
                return jsonify({'result': "ok"}), 201
            else:
                return jsonify({'message': 'User already registered'}), 500
        

        else:
            return jsonify({'message': 'Internal server error'}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()


@app.route('/change-email', methods=['POST'])
def change_email():
    try:
        data = request.json
        old_email = data.get('email')
        new_email = data.get('new_email')
        password = data.get('password')
        # print("Email: ", email)
        if not old_email or not new_email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_users WHERE email = %s"	, (new_email,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            return jsonify({'message': 'New email already in use'}), 403
        cursor.execute("SELECT * FROM flutter_users WHERE email = %s"	, (email,))
        connection.commit()
        response = cursor.fetchone()
        print(response)
        if (response):
            password_hash = response["password"] 

            if not check_password_hash(password_hash, password+config["ROACH_KING"]):
                return jsonify({'message': 'Invalid credentials'}), 403

            token = changeEmailLink(old_email, new_email, response["name"], "changeEmail", config)
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

@app.route('/validate-change-email-token', methods=['POST'])
def validate_change_email_token():
    try:
        data = request.json
        token = data.get('token')
        print("Token: ", token, "Length: ", len(token))
        if not token:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_dumpster WHERE data = %s"	, (token,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            old_email, new_email, exp = decodeChangeEmailToken(token, config)
            if datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(exp):
                return jsonify({'message': 'Token expired'}), 403
            else:
                cursor.execute("UPDATE flutter_users SET email = %s WHERE email = %s"	, (new_email, old_email))
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/complete-email-reset', methods=['POST'])
def complete_email_reset():
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
                print("Expired token")
                return jsonify({'message': 'Token expired'}), 403
            else:
                cursor.execute("UPDATE flutter_users SET  email = %s WHERE email = %s RETURNING *", (new_email, email))
                notify_about_email_change(email, new_email, response["name"], config)
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            print("Invalid token")
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/password-reset', methods=['POST'])
def password_reset():
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

@app.route('/validate-password-reset-token', methods=['POST'])
def validate_password_reset_token():
    try:
        data = request.json
        token = data.get('token')
        print("Token: ", token, "Length: ", len(token))
        if not token:
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
                return jsonify({'result': "ok"}), 201
        else:
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/complete-password-reset', methods=['POST'])
def complete_password_reset():
    try:
        data = request.json
        token = data.get('token')
        password = data.get('password') + config["ROACH_KING"]
        password_hash = generate_password_hash(password)
        if not token or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM flutter_dumpster WHERE data = %s"	, (token,))
        connection.commit()
        response = cursor.fetchone()
        if (response):
            email, exp = decodeResetToken(token, config)
            if datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(exp):
                print("Expired token")
                return jsonify({'message': 'Token expired'}), 403
            else:
                cursor.execute("UPDATE flutter_users SET  password = %s WHERE email = %s RETURNING *", (password_hash, email))
                connection.commit()
                return jsonify({'result': "ok"}), 201
        else:
            print("Invalid token")
            return jsonify({'message': 'Invalid token'}), 403
    except Exception as error:
        print('Error', error)
        return jsonify({'message': error}), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.json
        token = data.get('token')
        name = data.get('name')
        email = data.get('email')
        if email != recruiterVerification(token, config):
            return jsonify({'message': 'Invalid token'}), 403
        password = data.get('password') + config["ROACH_KING"]
        password_hash = generate_password_hash(password)
        print("PASSWORD HASH: ", password_hash)
        if not email or not name or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET name = %s, password = %s WHERE email = %s RETURNING *", (name, password_hash, email))
        
        connection.commit()
        result = cursor.fetchone()
        del result['password']
        return jsonify({'result': result}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/change-password', methods=['POST'])
def change_password():
    try:
        data = request.json
        new_password = data.get('newPassword')
        old_password = data.get('oldPassword')
        email = data.get('email')
        if not email or not new_password or not old_password :
            return jsonify({'message': 'Invalid input'}), HTTPStatus.BAD_REQUEST.value
        cursor = connection.cursor()
        cursor.execute("SELECT * from flutter_users WHERE email = %s", (email,))
        connection.commit()
        result = cursor.fetchone()
        if result:
            print("RESULT: ", result)
            password_hash = result["password"] 

            if check_password_hash(password_hash, old_password+config["ROACH_KING"]):
                pass
                
            else:
                return jsonify({'message': 'Invalid credentials'}), HTTPStatus.FORBIDDEN.value
        else:
            return jsonify({'message': 'Not a registered user'}), HTTPStatus.NOT_FOUND.value

        password = data.get('new_password') + config["ROACH_KING"]
        password_hash = generate_password_hash(password)

        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SETpassword = %s WHERE email = %s RETURNING *", (password_hash, email))
        
        connection.commit()
        result = cursor.fetchone()
        del result['password']
        return jsonify({'result': result}), HTTPStatus.OK.value
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json
        email = data.get('email')
        subscription_type = data.get('subscription_type')
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET subscription_type = %s WHERE email = %s", (subscription_type, email))
        
        connection.commit()
        # result = cursor.fetchone()
        return jsonify({'result': 'ok'}), 201
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT * from flutter_users WHERE email = %s", (email,))
        connection.commit()
        result = cursor.fetchone()
        if result:
            print("RESULT: ", result)
            password_hash = result["password"] 

            if check_password_hash(password_hash, password+config["ROACH_KING"]):
                reply = result
                del reply["password"]
                return jsonify({'result': reply}), HTTPStatus.OK.value
            else:
                return jsonify({'message': 'Invalid credentials'}), 403
        else:
            return jsonify({'message': 'Not a registered user'}), HTTPStatus.NOT_FOUND.value
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()


def get_stripe_customer(email):
    try:
        if not email:
            return {'message': 'Invalid input data'}
        cursor = connection.cursor()
        cursor.execute("SELECT customer_id from flutter_users WHERE email = %s", (email,))
        connection.commit()
        result = cursor.fetchone()
        if result:
            print("RESULT: ", result)
            return {'customerId': result["customer_id"]}	
        else: 
            return {'customerId': None}	
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return {'message': 'Internal server error'}
    finally:
        if 'cursor' in locals():
            cursor.close()

def set_stripe_customer(email, customer_id, subscription_type):
    try:
        if not email:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET customer_id = %s, subscription_type = %s WHERE email = %s", (customer_id, subscription_type, email,))
        connection.commit()
        # print("PUSHED STRIPE SESSION: ", stripe_session)	
        return {'result': "ok"}

    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return {'message': 'Internal server error'}
    finally:
        if 'cursor' in locals():
            cursor.close()

def set_stripe_subscription(customer_id, subscription_type):
    try:
        if not customer_id:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET  subscription_type = %s WHERE customer_id = %s", ( subscription_type, customer_id,))
        connection.commit()
        # print("PUSHED STRIPE SESSION: ", stripe_session)	
        return {'result': "ok"}

    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return {'message': 'Internal server error'}
    finally:
        if 'cursor' in locals():
            cursor.close()




@app.route('/books')
def get_books():    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()        
        return jsonify({'books': results})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.json
        isbn = data.get('isbn')
        name = data.get('name')
        cant_pages = data.get('cant_pages')
        author_id = data.get('author_id')
        if not name or not cant_pages or not author_id or not isbn:
            return jsonify({'message': 'Bad request, isbn or name or cantPages or author not found'}), 400
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO books (isbn, name, cant_pages, author_id) 
            VALUES (%s, %s, %s, %s) RETURNING book_id, isbn, name, cant_pages, author_id, created_at
            """, 
        (isbn, name, cant_pages, author_id))
        connection.commit()
        result = cursor.fetchone()
        return jsonify({'book': result}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

def close_connection():
    if 'connection' in globals():
        connection.close()
        print('Connection to the database closed')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
    atexit.register(close_connection)