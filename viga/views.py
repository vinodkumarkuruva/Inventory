from flask import request,jsonify, make_response
from viga import app,db
from .models import Inventory
import time,os


@app.route('/transform', methods=['POST'])
def transform():
    time.sleep(10)  # Simulating delay
    data = request.json
    print(f"Received transform data: {data}")
    return jsonify({"message": "Transform received", "data": data}), 200

@app.route('/translation', methods=['POST'])
def translation():
    time.sleep(10)
    data = request.json
    print(f"Received translation data: {data}")
    return jsonify({"message": "Translation received", "data": data}), 200

@app.route('/rotation', methods=['POST'])
def rotation():
    time.sleep(10)
    data = request.json
    print(f"Received rotation data: {data}")
    return jsonify({"message": "Rotation received", "data": data}), 200

@app.route('/scale', methods=['POST'])
def scale():
    time.sleep(10)
    data = request.json
    print(f"Received scale data: {data}")
    return jsonify({"message": "Scale received", "data": data}), 200

@app.route('/file-path', methods=['GET'])
def file_path():
    project_path = request.args.get('projectpath', 'false').lower() == 'true'
    file_path = "C:/example_project/example_file.blend"  # Example path
    return jsonify({"file_path": os.path.dirname(file_path) if project_path else file_path})

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    name, quantity = data.get('name'), data.get('quantity')
    if not name or quantity is None:
        return jsonify({"error": "Missing item name or quantity"}), 400
    try:
        # When adding an item, set both the quantity and max_quantity
        item = Inventory(name=name, quantity=quantity, max_quantity=quantity if quantity is not None else 0)
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item added", "name": name, "quantity": quantity, "max_quantity": quantity}), 200
    except:
        db.session.rollback()
        return jsonify({"error": "Item already exists"}), 400


@app.route('/buy-item', methods=['POST'])
def buy_item():
    """Decrease the quantity of an item (simulate buying an item)"""
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing item name"}), 400
    item = Inventory.query.filter_by(name=name).first()
    if item:
        if item.quantity > 0:
            item.quantity -= 1  # Reduce the quantity when buying
            db.session.commit()
            return jsonify({"message": "Item purchased", "name": name}), 200
        else:
            return jsonify({"error": "Item out of stock"}), 400
    return jsonify({"error": "Item not found"}), 404


@app.route('/return-item', methods=['POST'])
def return_item():
    """Increase the quantity of an item when returned, but do not exceed max_quantity"""
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing item name"}), 400
    
    item = Inventory.query.filter_by(name=name).first()
    if item:
        if item.quantity < item.max_quantity:
            item.quantity += 1  # Increase the quantity when returning
            db.session.commit()
            return jsonify({"message": "Item returned", "name": name, "new_quantity": item.quantity}), 200
        else:
            return jsonify({"error": "Cannot return item. Maximum stock reached."}), 400
    return jsonify({"error": "Item not found"}), 404




@app.route('/remove-item', methods=['POST'])
def remove_item():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Missing item name"}), 400
    item = Inventory.query.filter_by(name=name).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed"}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    name, quantity = data.get('name'), data.get('quantity')
    if not name or quantity is None:
        return jsonify({"error": "Missing item name or quantity"}), 400
    item = Inventory.query.filter_by(name=name).first()
    if item:
        item.quantity = quantity  # Update quantity
        item.max_quantity = quantity  # Update max_quantity as well
        db.session.commit()
        return jsonify({"message": "Quantity and max_quantity updated", "name": name, "new_quantity": item.quantity, "new_max_quantity": item.max_quantity}), 200
    return jsonify({"error": "Item not found"}), 404



@app.route('/inventory', methods=['GET'])
def get_inventory():
    """Fetch all inventory items from the database"""
    items = Inventory.query.all()  # Retrieve all items from the database
    inventory_data = {item.name: item.quantity for item in items}  # Convert to dictionary
    return jsonify(inventory_data), 200  # Return data as JSON
