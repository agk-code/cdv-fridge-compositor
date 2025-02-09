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

# In-memory storage for fridge items
fridge_items = [
    {"name": "Milk", "quantity": 2},
    {"name": "Eggs", "quantity": 12},
    {"name": "Cheese", "quantity": 1}
]

# Helper function to find an item by name
def find_item(name):
    return next((item for item in fridge_items if item["name"] == name), None)

# Get all fridge items
@app.route('/api/fridge', methods=['GET'])
def get_fridge_items():
    return jsonify(fridge_items)

# Add an item to the fridge
@app.route('/api/fridge', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')

    if not name or not quantity:
        return jsonify({"error": "Name and quantity are required"}), 400

    existing_item = find_item(name)
    if existing_item:
        return jsonify({"error": "Item already exists"}), 400

    fridge_items.append({"name": name, "quantity": quantity})
    return jsonify({"message": "Item added successfully"}), 201

# Update the quantity of an item
@app.route('/api/fridge/<string:name>', methods=['PUT'])
def update_item(name):
    data = request.get_json()
    quantity = data.get('quantity')

    if not quantity:
        return jsonify({"error": "Quantity is required"}), 400

    item = find_item(name)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    item["quantity"] = quantity
    return jsonify({"message": "Item updated successfully"})

# Delete an item from the fridge
@app.route('/api/fridge/<string:name>', methods=['DELETE'])
def delete_item(name):
    item = find_item(name)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    fridge_items.remove(item)
    return jsonify({"message": "Item deleted successfully"})

# Start the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)