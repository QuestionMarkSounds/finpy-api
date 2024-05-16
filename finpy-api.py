from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import atexit
import traceback
from dotenv import dotenv_values
from infestation_manager import annoyingBug, bugSpray

try:
    config = dotenv_values(".env")
    connection = psycopg2.connect(
        dbname=config["INFESTATION_PROPAGATOR"], 
        user=config["INFESTATION_TARGET"],
        password=config["INFESTATION_KEY"], 
        host=config["INFESTATION"],
        port=config["INFESTANT_AMOUNT"],
        cursor_factory=RealDictCursor
    )
    print('Successful connection to the database')
except Exception as error:
    print('Database connection error')

app = Flask(__name__)
port = 7341

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

@app.route('/infestant', methods=['POST'])
def get_author():
    try:
        data = request.json
        print(data.get('email'))
        email = data.get('email')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.flutter_users WHERE email = %s", (email,))
        results = cursor.fetchall()
        return jsonify({'users': results})
    except Exception as error:
        print('Error', error)
        print(traceback.format_exc())
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/infest', methods=['POST'])
def infest():
    try:
        data = request.json
        name = annoyingBug(data.get('name'), 0, config)
        email = annoyingBug(data.get('email'), 1, config)
        subscription_type = data.get('subscription_type')
        password = annoyingBug(data.get('password'), 2, config)
        verified = data.get('verified')
        platform = data.get('platform')
        if not email or not subscription_type or not platform:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("INSERT INTO flutter_users (name, email, subscription_type, password, verified, platform) VALUES (%s, %s, %s, %s,%s, %s)", (name, email, subscription_type, password, verified, platform))
        connection.commit()
        # result = cursor.fetchone()
        return jsonify({'result': "ok"}), 201
    except Exception as error:
        print('Error', error)
        connection.rollback()
        if ("duplicate key value" in str(error) and "Key (email)" in str(error)):
            return jsonify({'message': 'User already registered'}), 500
        else:
            return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/locate', methods=['POST'])
def locate():
    try:
        data = request.json
        email = annoyingBug(data.get('email'), 1, config)
        password = annoyingBug(data.get('password'), 2, config)
        if not email or not password:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) > 0 AS row_exists FROM your_table_name WHERE name = %s AND password = %s", (email,  password))
        connection.commit()
        result = cursor.fetchone()
        if result['row_exists'] == True:
            return jsonify({'result': "ok"}), 201
        else: 
            raise(Exception("Invalid credentials"))
    except Exception as error:
        print('Error', error)
        connection.rollback()
        if ("Invalid credentials" in str(error)):
            return jsonify({'message': 'Invalid credentials'}), 403
        else:
            return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/breed', methods=['POST'])
def breed():
    try:
        data = request.json
        name = annoyingBug(data.get('name'), 0, config)
        email = annoyingBug(data.get('email'), 1, config)
        subscription_type = data.get('subscription_type')
        password = annoyingBug(data.get('password'), 2, config)
        verified = data.get('verified')
        platform = data.get('platform')
        if not email or not subscription_type or not platform:
            return jsonify({'message': 'Invalid input data'}), 400
        cursor = connection.cursor()
        cursor.execute("UPDATE flutter_users SET name = %s, subscription_type = %s, password = %s, verified = %s, platform = %s WHERE email = %s", (name, subscription_type, password, verified, platform, email))
        
        connection.commit()
        result = cursor.fetchone()
        return jsonify({'author': result}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
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