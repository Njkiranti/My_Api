from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB Atlas connection string
client = None
try:
    client = MongoClient('mongodb+srv://njkiranti0:Kirantinj57@portfolio.lnaix.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio') 
    db = client['my_portfolio']  
    print("Connected to MongoDB")
except ConnectionFailure:
    print("Failed to connect to MongoDB")

# Helper function to get collection by name
def get_collection(collection_name):
    return db[collection_name]

# Get all collection names
@app.route('/collections', methods=['GET'])
def get_collections():
    collections = db.list_collection_names()
    return jsonify(collections)

# Get all items from all collections
@app.route('/all-items', methods=['GET'])
def get_all_items():
    all_items = {}
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        items = list(collection.find({}, {'_id': 0}))
        all_items[collection_name] = items
    return jsonify(all_items)

# Get all items from a about_me
@app.route('/about_me', methods=['GET'])
def get_about_me():
    collection = db["about_me"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)


# Get all items from a clients_reviews
@app.route('/clients_reviews', methods=['GET'])
def get_clients_reviews(collection_name):
    collection = db["clients_reviews"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a contact
@app.route('/contact', methods=['GET'])
def get_contact():
    collection = db["contact"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a docs
@app.route('/docs', methods=['GET'])
def get_docs():
    collection = db["docs"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a links
@app.route('/links', methods=['GET'])
def get_links():
    collection = db["links"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a my_experience
@app.route('/my_experience', methods=['GET'])
def get_my_experience():
    collection = db["my_experience"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a my_projects
@app.route('/my_projects', methods=['GET'])
def get_my_projects():
    collection = db["my_projects"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)


# Get all items from a my_services
@app.route('/my_services', methods=['GET'])
def get_my_services():
    collection = db["my_services"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

# Get all items from a my_skills
@app.route('/my_skills', methods=['GET'])
def get_my_skills():
    collection = db["my_skills"]
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)


# Get a single item by name from a specific collection
@app.route('/items/<string:collection_name>/<string:name>', methods=['GET'])
def get_item(collection_name, name):
    collection = db[collection_name]
    item = collection.find_one({"name": name}, {'_id': 0})
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404
    

# Create a new item in a specific collection
@app.route('/items/<string:collection_name>', methods=['POST'])
def create_item(collection_name):
    collection = db[collection_name]
    new_item = request.json
    collection.insert_one(new_item)
    return jsonify(new_item), 201

# Update an existing item in a specific collection
@app.route('/items/<string:collection_name>/<string:name>', methods=['PUT'])
def update_item(collection_name, name):
    collection = db[collection_name]
    data = request.json
    result = collection.update_one({"name": name}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Item updated"})
    else:
        return jsonify({"error": "Item not found"}), 404

# Delete an item from a specific collection
@app.route('/items/<string:collection_name>/<string:name>', methods=['DELETE'])
def delete_item(collection_name, name):
    collection = db[collection_name]
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": "Item deleted"})
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
