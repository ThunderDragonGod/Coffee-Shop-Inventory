from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection details (replace these with your own)
MONGO_URI = 'mongodb://localhost:27017/'  # Example MongoDB URI (use your own URI if needed)
DB_NAME = 'Coffee'          # Your existing database name
COLLECTION_NAME = 'Order History'  # Your existing collection name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Route for the main options page (default landing page)
@app.route('/')
def index1():
    return render_template('index1.html')

# Route to view inventory
@app.route('/inventory')
def index():
    # Fetch all items from MongoDB
    inventory = list(collection.find())
    return render_template('index.html', inventory=inventory)

# Route to add a new item to the inventory
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        # Insert item into MongoDB (using existing collection)
        collection.insert_one({'item_name': item_name, 'quantity': quantity})
        return redirect(url_for('index'))
    return render_template('add_item.html')

# Route to update an item's quantity
@app.route('/update_item/<item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    # Find the item by ObjectId
    item = collection.find_one({'_id': ObjectId(item_id)})

    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        # Update item in MongoDB
        collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {'item_name': item_name, 'quantity': quantity}}
        )
        return redirect(url_for('index'))

    # Pass the single item (not a list) to the template
    return render_template('update_item.html', item=item)

# Route to delete an item from the inventory
@app.route('/delete_item', methods=['POST'])
def delete_item():
    # Get the item ID from the form
    item_id = request.form['item_id']
    # Delete the item by ObjectId
    collection.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))

# Route to check item availability
@app.route('/enquire', methods=['GET', 'POST'])
def enquire():
    availability = None
    if request.method == 'POST':
        item_name = request.form['item_name']
        # Check if item exists in the collection
        item = collection.find_one({'item_name': item_name})
        availability = 'Available' if item else 'Not Available'
    
    return render_template('enquire.html', availability=availability)

if __name__ == '__main__':
    app.run(debug=True)
