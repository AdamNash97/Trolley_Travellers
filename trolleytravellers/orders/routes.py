from flask import Blueprint, jsonify, abort, request
from trolleytravellers import db
from trolleytravellers.models import Order, OrderSchema, OrderSchemas
from trolleytravellers.main.utils import get_current_date
from trolleytravellers.orders.utils import find_volunteer_match

orders = Blueprint('orders', __name__)

order_schema = OrderSchema(many=True)

@orders.route('/order_list', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    output = order_schema.dump(orders)
    return jsonify({'order' : output})
    
@orders.route('/order/<id>', methods=['GET'])
def list_order():
    try:
        order = Order.query.get(id)
        order_schema = OrderSchema()
        return order_schema.jsonify(order)
    except:
         abort(400)

@orders.route('/add_order', methods=['POST'])
def new_order():
    try:
        order_date = request.json['order_date']
        customer_id = request.json['customer_id']
        volunteer_id = request.json['volunteer_id']
        new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id)
        db.session.add(new_order)
        db.session.commit()
        order_schema = OrderSchema()
        return order_schema.jsonify(new_order)
    except:
         abort(400)

@orders.route('/add_multiple_orders', methods=['POST'])
def new_orders():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            order_date = json_object.get('order_date')
            customer_id = json_object.get('customer_id')
            volunteer_id = json_object.get('volunteer_id')
            new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id)
            db.session.add(new_order)
            db.session.commit()
            order_schema = OrderSchema()
            order_schema.jsonify(new_order)
        orders = Order.query.all()
        output = order_schema.dump(orders)
        return jsonify({'# orders in database' : len(output)})
    except:
        abort(400)


@orders.route('/update_order/<id>', methods=['PUT'])
def update_order(id):
    try:
        order = Order.query.get(id)
        order_date = request.json['order_date']
        customer_id = request.json['customer_id']
        volunteer_id = request.json['volunteer_id']
    
        order.order_date = order_date
        order.customer_id = customer_id
        order.volunteer_id = volunteer_id
      
        db.session.commit()
        order_schema = OrderSchema()
        return order_schema.jsonify(order)
    except:
         abort(404)

@orders.route('/delete_order/<id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        order_schema = OrderSchema()
        return order_schema.jsonify({order})
    except:
        abort(404)

#Just need to pass in a customer_id in the body when making the request
#Will later need to add in if/else statement to handle the case when there
#are no matching volunteers, but for now we are guaranteed a match using our
#mock data.
@orders.route('/place_order_and_find_volunteer', methods=['POST'])
def place_order_and_find_volunteer():
    try:
        order_date = get_current_date()
        customer_id = request.json['customer_id']
        volunteer_id = find_volunteer_match(int(customer_id))
        new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id)
        db.session.add(new_order)
        db.session.commit()
        order_schema = OrderSchemas()
        return order_schema.jsonify(new_order)
    except:
         abort(400)