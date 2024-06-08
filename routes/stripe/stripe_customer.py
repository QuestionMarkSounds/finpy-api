import traceback
from flask import jsonify


def set_stripe_subscription(customer_id, subscription_type, connection):
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


def get_stripe_customer(email, connection):
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


