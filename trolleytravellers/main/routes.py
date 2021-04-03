from flask import Blueprint, jsonify, request, abort
from trolleytravellers import db
from trolleytravellers.models import Customer, CustomerSchema, Volunteer, VolunteerSchema

main = Blueprint('main', __name__)

@main.route('/customer_list', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    output = customer_schema.dump(customers)
    return jsonify({'customer' : output})

@main.route('/single_customer/<id>', methods=['GET'])
def list_customer(id):
    try:
        customer = Customer.query.get(id)
        customer_schema = CustomerSchema()
        return customer_schema.jsonify({customer})
    except:
        abort(404)

@main.route('/add_customer', methods=['POST'])
def new_customer():
    try:
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']
        new_customer = Customer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
        db.session.add(new_customer)
        db.session.commit()
        customer_schema = CustomerSchema()
        return customer_schema.jsonify(new_customer)
    except:
         abort(400)

@main.route('/add_multiple_customers', methods=['POST'])
def new_customers():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            email_data = json_object.get('email')
            username_data = json_object.get('username')
            password_data = json_object.get('password')
            postcode_data = json_object.get('postcode')
            house_number_data = json_object.get('house_number')
            new_customer = Customer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
            db.session.add(new_customer)
            db.session.commit()
            customer_schema = CustomerSchema()
            customer_schema.jsonify(new_customer)
        return jsonify({'# customers in database' : new_customer.id})
    except:
         abort(400)

@main.route('/update_customer<id>', methods=['POST'])
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
        customer.password = password_data
        customer.postcode = postcode_data
        customer.house_number = house_number_data
       
        db.session.commit()

        customer_schema = CustomerSchema()
        return customer_schema.jsonify(customer)
    except:
         abort(404)

@main.route('/delete_customer/<id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        db.session.delete(customer)
        db.session.commit()
        customer_schema = CustomerSchema()
        return customer_schema.jsonify({customer})
    except:
        abort(404)

@main.route('/volunteer_list', methods=['GET'])
def list_volunteers():
    volunteers = Volunteer.query.all()
    volunteer_schema = VolunteerSchema(many=True)
    output = volunteer_schema.dump(volunteers)
    return jsonify({'volunteer' : output})

@main.route('/single_volunteer/<id>', methods=['GET'])
def list_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify({volunteer})
    except:
        abort(404)

@main.route('/add_volunteer', methods=['POST'])
def new_volunteer():
    try:
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']
        new_volunteer = Volunteer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
        db.session.add(new_volunteer)
        db.session.commit()
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify(new_volunteer)
    except:
         abort(400)

@main.route('/update_volunteer<id>', methods=['POST'])
def update_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        email_data = request.json['email']
        username_data = request.json['username']
        password_data = request.json['password']
        postcode_data = request.json['postcode']
        house_number_data = request.json['house_number']

        volunteer.email = email_data
        volunteer.username = username_data
        volunteer.password = password_data
        volunteer.postcode = postcode_data
        volunteer.house_number = house_number_data
       
        db.session.commit()

        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify(volunteer)
    except:
         abort(404)

@main.route('/add_multiple_volunteers', methods=['POST'])
def new_volunteers():
    try:
        jsonBody = request.get_json()
        for json_object in jsonBody:
            email_data = json_object.get('email')
            username_data = json_object.get('username')
            password_data = json_object.get('password')
            postcode_data = json_object.get('postcode')
            house_number_data = json_object.get('house_number')
            new_volunteer = Volunteer(email=email_data, username=username_data, password=password_data, postcode=postcode_data, house_number=house_number_data)
            db.session.add(new_volunteer)
            db.session.commit()
            volunteer_schema = VolunteerSchema()
            volunteer_schema.jsonify(new_volunteer)
        return jsonify({'# volunteers in database' : new_volunteer.id})
    except:
         abort(400)

@main.route('/delete_volunteer/<id>', methods=['DELETE'])
def delete_volunteer(id):
    try:
        volunteer = Volunteer.query.get(id)
        db.session.delete(volunteer)
        db.session.commit()
        volunteer_schema = VolunteerSchema()
        return volunteer_schema.jsonify({volunteer})
    except:
        abort(404)



