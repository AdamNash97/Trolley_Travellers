from flask import Blueprint, jsonify, abort, request 
import json
from trolleytravellers import db, mail
from trolleytravellers.models import Order, OrderProduct, OrderSchema, Status, Customer, Volunteer, OrderProductSchema
from trolleytravellers.main.utils import get_current_date
from trolleytravellers.orders.utils import find_volunteer_match, create_connection, create_shopping_list
from flask_mail import Message
database = r"./trolleytravellers/site.db"


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
        status = Status.PENDING
        new_order = Order(order_date=order_date, customer_id=customer_id, volunteer_id=volunteer_id, status=status)
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
        
        if volunteer_id == 0:
            
            abort(500)
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
# {json.dumps([f"Number of {product_name}: {quantity}" for product_name, quantity in shopping_list[1]])}
        msg.body = f'''Hi {current_customer.username}!

Order number: {order_id}

Your order has been submitted and is now {status.name}. 
You have been matched with volunteer number {volunteer_id}, who lives in your local area. 
Thanks to them, your items will be with you soon.

Your volunteer will be bringing you the following order to your doorstep:

{newline.join(f"Number of {product_name}: {quantity}" for product_name, quantity in shopping_list[1])}


Total cost of your shopping: 

Thank you for using TrolleyTravellers!'''

        mail.send(msg)
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

@orders.route('/order_completed', methods=['PUT'])
def set_order_as_completed():
    order_id = request.json['order_id']
    current_order = Order.query.get(int(order_id))
    current_order.status = Status.COMPLETED
    (current_order.volunteer).engaged = 0
    db.session.commit()
    order_schema = OrderSchema()
    return order_schema.jsonify(current_order)


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
    order_schema = OrderSchema()
    return order_schema.jsonify(current_order)

#@orders.route('/order_cancelled/<token>', methods=['GET', 'POST'])
def cancellation_token(token):
    current_customer_token = Customer.verify_cancellation_token(token)
    if current_customer_token is None:
        abort(403)
    return current_customer_token



# @orders.route('/create_shopping_list', methods=['POST'])
# def add_product():
#     """
#     ACCESS TO PRODUCT TABLE -> SELECT SPECIFIC PRODUCT USING A NAME -> 
#     ASSIGN A QUANTITY TO THAT PRODUCT -> USE FOREIGN KEY TO ACCESS PRODUCT ID -> 
#     USE ID AND QUANTITY TO CREATE NEW ORDER_PRODUCT
#     """
#     #try:
#         #customer_id = request.json['customer_id']
#     #BODY: list of product names
#     # Validate items: list of prouduct names in shopping list
#     # If in db, retrieve product id, add to shopping list
#     product_names = request.json['product_names']
#     conn = create_connection(database)
#     cur = conn.cursor()
#     shopping_list, initial_shopping_list = [], []
#     cur.execute(f"SELECT id, name FROM product")
#     product_rows = cur.fetchall()

#     all_items = {} 
#     for product in product_rows:
#         all_items[product[1]] = str(product[0]) # dictionary (product name: product id)

# # appends product ids to initial_shopping_list via dictionary
#     for product in product_names:
#         if product in all_items:
#             initial_shopping_list.append(all_items[str(product)]) 
            
#     # One column list of product ids, perform counting, deletion and quantity variables
#     shopping_list = [ [product, initial_shopping_list.count(product)] for product 
#     in list(set(initial_shopping_list)) ] # [ [product, quantity], [product, quantity], ...,
#                                           # [product, quantity] ]
#     conn.close()

#     return json.dumps(shopping_list)
    # return json.dumps(product_rows[0][0]) # 1 (product ids)
    # return json.dumps(product_rows[0][1]) # "Whmis Spray Bottle Graduated" (product names)
    # except:
    
    #     abort(400)

        # {"product_names": ["Yucca", "Rhubarb","Yucca"]}
        #{"product_names": ["Whmis Spray Bottle Graduated", "Yucca", "Yucca"]}

        #ORDER (Assertion for SHOPPING LIST AND PRODUCT LIST)
        ##list of items in shopping basket
        ###Prodcuts inventory

        #ORDER PRODUCT(Assertion between Prodcut list and order)
        ##Order already been made
        ###Prodcuts inventory

        #SHOPPING_LIST (tuple -> order id: product id)
        #OPEN ORDER REQUEST - GENERATES ORDER ID
        #append customers choice: Order Id: product id
        # Counting for loop for instances of each product id - Count method
        #that geerates quantity values
        # order_111.product_id.append_all(product_id=[18495, 19284, 20495])
