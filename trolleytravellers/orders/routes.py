from flask import Blueprint, jsonify, abort, request 
import json
from trolleytravellers import db, mail
from trolleytravellers.models import Order, OrderProduct, OrderSchema, Status, Customer, Volunteer, OrderProductSchema, Product
from trolleytravellers.main.utils import get_current_date_as_string
from trolleytravellers.orders.utils import find_volunteer_match, create_connection, create_shopping_list
from flask_mail import Message

orders = Blueprint('orders', __name__)

# Read in database link
database = r"./trolleytravellers/site.db"

# Order schema initialisation to be used multiple times in this file
order_schema = OrderSchema(many=True)

# List all orders in the database
@orders.route('/order_list', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    output = order_schema.dump(orders)
    return jsonify({'order' : output})

# Display all columns of a specific order
@orders.route('/order/<id>', methods=['GET'])
def list_order(id):
    try:
        order = Order.query.get(id)
        order_schema = OrderSchema()
        return order_schema.jsonify(order)
    except:
         abort(400)

# List all orders by a particular customer
@orders.route('/customer_order_history/<id>', methods=['GET'])
def list_customer_order_history(id):
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute('SELECT * FROM "order"') # quotes required because order is a reserved word.
        orders = cur.fetchall()
        customer_order_history = []
        for order in orders:
            if str(order[2]) == str(id):
                customer_order_history.append(order)
        conn.close()
        newline = "\n"
        return newline.join(f"Order ID: {order_id}, Date: {order_date}, Customer ID: {customer_id}, Volunteer ID: {volunteer_id}, Order Status: {order_status}" 
        for order_id, order_date, customer_id, volunteer_id, order_status in customer_order_history)
    except:
        abort(400)

# Route for adding an order
@orders.route('/add_order', methods=['POST'])
def new_order():
    try:
        order_date = request.json['order_date']
        customer_id = request.json['customer_id']
        volunteer_id = request.json['volunteer_id']
        status = Status.PENDING
        new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id, status=status)
        db.session.add(new_order)
        db.session.commit()
        order_schema = OrderSchema()
        return order_schema.jsonify(new_order)
    except:
         abort(400)

# Route for adding multiple orders
@orders.route('/add_multiple_orders', methods=['POST'])
def new_orders():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            order_date = json_object.get('order_date')
            customer_id = json_object.get('customer_id')
            volunteer_id = json_object.get('volunteer_id')
            status = Status.PENDING
            new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id, status=status)
            db.session.add(new_order)
            db.session.commit()
            order_schema = OrderSchema()
            order_schema.jsonify(new_order)
        orders = Order.query.all()
        output = order_schema.dump(orders)
        return jsonify({'# orders in database' : len(output)})
    except:
        abort(400)

# Update existing order by id
@orders.route('/update_order/<id>', methods=['PUT'])
def update_order(id):
    try:
        order = Order.query.get(id)
        order_date = request.json['order_date']
        customer_id = request.json['customer_id']
        volunteer_id = request.json['volunteer_id']
        status = Status.PENDING
        order.order_date = order_date
        order.customer_id = customer_id
        order.volunteer_id = volunteer_id
        order.status = status
        db.session.commit()
        order_schema = OrderSchema()
        return order_schema.jsonify(order)
    except:
         abort(404)

# Delete existing order by id
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

"""
Super route which generates a volunteer-customer match AND creates an order AND sends emails to the 
parties involved to let them know about their order.
"""
@orders.route('/place_order_and_find_volunteer', methods=['POST'])
def place_order_and_find_volunteer():
    try:
        order_date = get_current_date_as_string()
        customer_id = request.json['customer_id']
        volunteer_id = find_volunteer_match(int(customer_id))
        
        if volunteer_id == 0:
            current_customer = Customer.query.get(int(customer_id))

            msg = Message('Volunteers Unavailable',
                  sender='trolleytravellers@gmail.com',
                  recipients=[current_customer.email])
            newline = "\n"

            msg.body = f'''
Hi {current_customer.username}!

Apologies, there are no volunteers currently available! Please try again later!

Thank you for using TrolleyTravellers!'''

            mail.send(msg)
        
            abort(503)
        #Set engaged status to true for matched volunteer
        (Volunteer.query.get(int(volunteer_id))).engaged = 1
        status = Status.PENDING
        new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id, status=status)
        db.session.add(new_order)
        db.session.commit()
        #current_order = Order.query.get(new_order.id)
        shopping_list = create_shopping_list()
        global new_order_id
        global new_order_ids
        new_product_ids = []
        for item in shopping_list[0]:
            order_id = new_order.id 
            product_id = item[0]
            quantity = item[1]
            new_order_product = OrderProduct(order_id = order_id, product_id=product_id, quantity=quantity)
            db.session.add(new_order_product)
            db.session.commit()
            new_order_id = new_order_product.order_id
            new_product_ids.append(new_order_product.product_id)
        #new order product here will contain products
        current_customer = Customer.query.get(int(customer_id))
        msg = Message('Order Submission Confirmation',
                  sender='trolleytravellers@gmail.com',
                  recipients=[current_customer.email])
        newline = "\n"
        msg.body = f'''
Hi {current_customer.username}!
Order number: {order_id}
Your order has been submitted and is now {status.name}. 
You have been matched with volunteer number {volunteer_id}, who lives in your local area. 
Thanks to them, your items will be with you soon.
Your volunteer will be bringing you the following order to your doorstep:
{newline.join(f"Number of {product_name}: {quantity}" for product_name, quantity in shopping_list[1])}
It will cost £{round(shopping_list[2], 2)}.
Thank you for using TrolleyTravellers!'''

        mail.send(msg)

        volunteer_message = Message('Customer Request Received',
                            sender='trolleytravellers@gmail.com',
                            recipients=[Volunteer.query.get(int(volunteer_id)).email])
        newline = "\n"
        volunteer_message.body = f'''
Hi {(Volunteer.query.get(int(volunteer_id))).username}! 
A volunteer in your local area has requested your help! The order is as follow:

{newline.join(f"Number of {product_name}: {quantity}" for product_name, quantity in shopping_list[1])}
It will cost £{round(shopping_list[2], 2)}. Please request this in cash from your customer when dropping it off.

Thank you for your service, without you TrolleyTravellers could not exist!
        '''
        mail.send(volunteer_message)

        order_product_schema = OrderProductSchema(many=True)
        new_orders_products = []
        for new_product_id in new_product_ids:
            # return json.dumps(new_order_id)
            new_orders_products.append(OrderProduct.query.get(  ( int(new_order_id), int(new_product_id) )  ))
        output = order_product_schema.dump(new_orders_products)
        token = current_customer.get_cancellation_token()
        return jsonify([{'Receipt' : output}, {'Token' : token}])
    except:
         abort(400)

# Mark order as completed by order_id using json input body
@orders.route('/order_completed', methods=['PUT'])
def set_order_as_completed():
    order_id = request.json['order_id']
    current_order = Order.query.get(int(order_id))
    current_order.status = Status.COMPLETED
    (current_order.volunteer).engaged = 0
    db.session.commit()
    order_schema = OrderSchema()
    return order_schema.jsonify(current_order)

# Mark order as cancelled passing order_id using json input body
@orders.route('/order_cancelled', methods=['PUT'])
def set_order_as_cancelled():
    jsonBody = request.get_json()
    global token_to_check

    for json_object in jsonBody:
        token_to_check = json_object.get('token')
        order_id = json_object.get('order_id')

    cancellation_token(token_to_check)
    current_order = Order.query.get(int(order_id))
    current_order.status = Status.CANCELLED
    (current_order.volunteer).engaged = 0
    db.session.commit()
    current_customer = Customer.query.get(current_order.customer_id)
    current_volunteer = Volunteer.query.get(current_order.volunteer_id)

    conn = create_connection(database)
    cur = conn.cursor()
    cancelled_shopping_list = []
    cur.execute("SELECT order_id, product_id, quantity FROM order_product")
    order_product_rows = cur.fetchall() # [ [order_id, product_id, quantity] ... ]
    for order_product in order_product_rows:
        if order_product[0] == order_id:
            product_name = (Product.query.get(order_product[1])).name # product_id -> product_name
            product_quantity = order_product[2] 
            cancelled_shopping_list.append( [ product_name, product_quantity ] )

    msg = Message('Order Cancellation Confirmation',
                  sender='trolleytravellers@gmail.com',
                  recipients=[current_customer.email, current_volunteer.email])
    newline = "\n"
    msg.body = f'''Hi!

Order number: {order_id}

Your order has been {current_order.status.name}. 

The following items are no longer being processed:
{newline.join(f"Number of {product_name}: {quantity}" for product_name, quantity in cancelled_shopping_list)}

Thank you for using TrolleyTravellers!'''

    mail.send(msg)
    order_schema = OrderSchema()
    return order_schema.jsonify(current_order)


# used in '/order_cancelled' route. Checks if the current customer is within cancellation period, if not throws 403 error
def cancellation_token(token):
    current_customer_token = Customer.verify_cancellation_token(token)
    if current_customer_token is None:
        abort(403)
    return current_customer_token

# Generates a shopping list to insert into order_product table
@orders.route('/create_shopping_list', methods=['POST'])
def add_product():
    try:
        product_names = request.json['product_names']
        conn = create_connection(database)
        cur = conn.cursor()
        shopping_list, initial_shopping_list = [], []
        cur.execute("SELECT id, name, price FROM product")
        product_rows = cur.fetchall()

        all_items = {} 
        for product in product_rows:
            all_items[product[1]] = str(product[0]) # dictionary (product name: product id)
            all_items[str(product[0])] = float(product[2]) # dictionary (product id: price)
        sum_of_shopping_list = 0
        # appends product ids to initial_shopping_list via dictionary

        initial_customer_shopping_list = []
        for product in product_names:
            if product in all_items:
                initial_shopping_list.append(all_items[str(product)]) # appends product ids to initial shopping list
                initial_customer_shopping_list.append(str(product))
        for item in initial_shopping_list:
            sum_of_shopping_list += all_items[str(item)]
                
        # One column list of product ids, perform counting, deletion and quantity variables
        shopping_list = [ [product, initial_shopping_list.count(product)] for product 
        in list(set(initial_shopping_list)) ] # [ [product, quantity], [product, quantity], ...,[product, quantity] ]
        
        customer_shopping_list = [ [ product, initial_customer_shopping_list.count(product) ] for product
        in list(set( initial_customer_shopping_list)) ] # [ [ product_name, quantity ] ... ]
        conn.close()
        list_of_shopping_lists = [shopping_list, customer_shopping_list, sum_of_shopping_list]
        return json.dumps(list_of_shopping_lists[1])
        
    except:
        abort(400)
