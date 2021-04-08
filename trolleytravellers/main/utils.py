from datetime import datetime
from trolleytravellers.models import Customer, Volunteer
from trolleytravellers import bcrypt

#Used to access current date for order_date attribute

def get_current_date():
    # Creating a datetime object so we can test.
    current_date = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    current_date = int(current_date.strftime('%Y%m%d'))
    return current_date

def get_current_date_as_string():
    # Creating a datetime object so we can test.
    current_date = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    timestamp_string = current_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp_string

#In models, convert order_date column type to string
#Reload the database

def is_authenticated_customer(customer_username, customer_password):
    customer_to_check = Customer.query.filter_by(username=str(customer_username)).first()
    if customer_to_check and bcrypt.check_password_hash(customer_to_check.password, customer_password):
        return True
    return False


def is_authenticated_volunteer(volunteer_username, volunteer_password):
    volunteer_to_check = Volunteer.query.filter_by(username=str(volunteer_username)).first()
    if volunteer_to_check and bcrypt.check_password_hash(volunteer_to_check.password, volunteer_password):
        return True
    return False


