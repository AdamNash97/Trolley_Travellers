from datetime import datetime
from trolleytravellers.models import Customer, Volunteer
from trolleytravellers import bcrypt

#Used to access current date for order_date attribute as integer
def get_current_date():
    current_date = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    current_date = int(current_date.strftime('%Y%m%d'))
    return current_date

#Used to access current date for order_date attribute as string
def get_current_date_as_string():
    current_date = datetime.now()
    timestamp_string = current_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp_string

def is_authenticated_customer(customer_username, customer_password):
    # Checks a given customer username's password against the database and returns the corresponding boolean
    customer_to_check = Customer.query.filter_by(username=str(customer_username)).first()
    if customer_to_check and bcrypt.check_password_hash(customer_to_check.password, customer_password):
        return True
    return False

def is_authenticated_volunteer(volunteer_username, volunteer_password):
    # Checks a given volunteer username's password against the database and returns the corresponding boolean
    volunteer_to_check = Volunteer.query.filter_by(username=str(volunteer_username)).first()
    if volunteer_to_check and bcrypt.check_password_hash(volunteer_to_check.password, volunteer_password):
        return True
    return False


