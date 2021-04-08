from flask import Blueprint, request, jsonify
from trolleytravellers.main.utils import is_authenticated_customer, is_authenticated_volunteer
main = Blueprint('main', __name__)

database = r"./trolleytravellers/site.db"

@main.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    json_body = request.get_json()

    customer_username, customer_password = "", ""

    for json_object in json_body:
        customer_username = json_object.get('username')
        customer_password = json_object.get('password')

    print(customer_username)
    logged_in = is_authenticated_customer(customer_username, customer_password)
    failed_login = 'Login details incorrect, or no account found.'
    if logged_in:
        return jsonify({'Logged In' : logged_in })
    else:
        return jsonify({'Login Failure' : failed_login })

            
@main.route('/volunteer_login', methods=['GET', 'POST'])
def volunteer_login():
    json_body = request.get_json()

    volunteer_username, volunteer_password = "", ""

    for json_object in json_body:
        volunteer_username = json_object.get('username')
        volunteer_password = json_object.get('password')
    

    logged_in = is_authenticated_volunteer(volunteer_username, volunteer_password)
    failed_login = 'Login details incorrect, or no account found.'
    if logged_in:
        return jsonify({'Logged In' : logged_in })
    else:
        return jsonify({'Login Failure' : failed_login })


    
