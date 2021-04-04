
#Combine all configuration in a single object to allow inheritance later.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

#Create database and add data in terminal:
#'python'
#'from trolleytravellers import db, create_app'
#'app = create_app()'
#'app.app_context().push()'
#'from trolleytravellers.models import Customer, Volunteer, Order'
#'db.create_all()'
#'customer_1 = Customer(email='adam@demo.com', username='adam', password='password', postcode='ST34QX',house_number='99')'
#'customer_2 = Customer(email='saif@demo.com', username='saif', password='passwor', postcode='ST25TY',house_number='56') ' 
#'db.session.add_all([customer_1, customer_2])'
#'db.session.commit()'
