import flask
import flask_cors
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import psycopg2
from psycopg2 import pool
import os
import json

app = Flask(__name__)
CORS(app, origins="*")

# Redis client for queueing
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'pepperoni'),
    port=os.getenv('REDIS_PORT', 6379)
)

# PostgreSQL connection pool
pg_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    host=os.getenv('POSTGRES_HOST', 'mushroom'),
    database=os.getenv('POSTGRES_DB', 'fridge')
)


# Get all items in the fridge
@app.route('/api/fridge', methods=['GET'])
def get_fridge_items():
    conn = pg_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM fridge')
            rows = cur.fetchall()
            response = flask.jsonify([{'name': row[1], 'quantity': row[2]} for row in rows])
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    finally:
        pg_pool.putconn(conn)

# Add or update an item in the fridge (queue the request in Redis)
@app.route('/api/fridge', methods=['POST'])
def add_fridge_item():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    request_data = {'type': 'add', 'name': name, 'quantity': quantity}
    try:
        redis_client.lpush('fridge-queue', json.dumps(request_data))
        return '', 200
    except Exception as e:
        print(f'Error queuing request: {e}')
        return 'Error queuing request', 500

# Update item quantity (queue the request in Redis)
@app.route('/api/fridge/<name>', methods=['PUT'])
def update_fridge_item(name):
    data = request.get_json()
    quantity = data.get('quantity')
    request_data = {'type': 'update', 'name': name, 'quantity': quantity}
    try:
        redis_client.lpush('fridge-queue', json.dumps(request_data))
        return '', 200
    except Exception as e:
        print(f'Error queuing request: {e}')
        return 'Error queuing request', 500

# Start the server
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)