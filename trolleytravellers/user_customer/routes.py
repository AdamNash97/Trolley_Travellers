from flask import Blueprint, jsonify, request, abort
from trolleytravellers import db, bcrypt
from trolleytravellers.models import Customer, CustomerSchema

user_customer = Blueprint('user_customer', __name__)

@user_customer.route('/customer_list', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    output = customer_schema.dump(customers)
    return jsonify({'customer' : output})

@user_customer.route('/single_customer/<id>', methods=['GET'])
def list_customer(id):
    try:
        customer = Customer.query.get(id)
        customer_schema = CustomerSchema()
        return customer_schema.jsonify(customer)
    except:
        abort(404)

@user_customer.route('/add_customer', methods=['POST'])
def new_customer():
    try:
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        #Hash password entered by user for storage in database.
        hashed_password = bcrypt.generate_password_hash(password_data).decode('utf-8')
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']
        new_customer = Customer(email=email_data, username=username_data, password=hashed_password, postcode=postcode_data, house_number=house_number_data)
        db.session.add(new_customer)
        db.session.commit()
        customer_schema = CustomerSchema()
        return customer_schema.jsonify(new_customer)
    except:
         abort(400)

@user_customer.route('/add_multiple_customers', methods=['POST'])
def new_customers():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            email_data = json_object.get('email')
            username_data = json_object.get('username')
            password_data = json_object.get('password')
            #Hash password entered by user for storage in database.
            hashed_password = bcrypt.generate_password_hash(password_data).decode('utf-8')
            postcode_data = json_object.get('postcode')
            house_number_data = json_object.get('house_number')
            new_customer = Customer(email=email_data, username=username_data, password=hashed_password, postcode=postcode_data, house_number=house_number_data)
            db.session.add(new_customer)
            db.session.commit()
            customer_schema = CustomerSchema()
            customer_schema.jsonify(new_customer)
        customers = Customer.query.all()
        customer_schema = CustomerSchema(many=True)
        output = customer_schema.dump(customers)
        return jsonify({'# customers in database' : len(output)})
    except:
         abort(400)

@user_customer.route('/update_customer/<id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = Customer.query.get(id)
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']

        customer.email = email_data
        customer.username = username_data
        #Hash password entered by user for storage in database.
        hashed_password = bcrypt.generate_password_hash(password_data).decode('utf-8')
        customer.password = hashed_password
        customer.postcode = postcode_data
        customer.house_number = house_number_data
       
        db.session.commit()

        customer_schema = CustomerSchema()
        return customer_schema.jsonify(customer)
    except:
         abort(404)

@user_customer.route('/delete_customer/<id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        db.session.delete(customer)
        db.session.commit()
        customer_schema = CustomerSchema()
        return customer_schema.jsonify({customer})
    except:
        abort(404)

        