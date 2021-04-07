import os
#Combine all configuration in a single object to allow inheritance later.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #Should ideally store in an environment variable locally and use os package to access: 
    SECRET_KEY = '7e9d2cb1f691ff74c8862c62df1502b6'
    #Configuration values needed for mail server:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    #TLS: Transport Layer Security - Cryptographic protocols for communication security over computer network.
    MAIL_USE_TLS = True
    #Ideally should store the username and password below on your local machine as environment variables.
    #I created a gmail business account for trolleytravellers to send the emails from.
    # MAIL_USERNAME = os.environ.get('EMAIL_TT')
    # MAIL_PASSWORD = os.environ.get('PASS_TT')
    MAIL_USERNAME = 'trolleytravellers@gmail.com'
    MAIL_PASSWORD = 'Trolleys2021'

#Creating the secret key:
#In python terminal:
#'import secrets'
#'secrets.token_hex(16)'
#https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask

#Create database and add data in terminal:
#'python'
#'from trolleytravellers import db, create_app'
#'app = create_app()'
#'app.app_context().push()'
#'from trolleytravellers.models import Customer, Volunteer, Order, Product, OrderProduct'
#'db.create_all()'
#'customer_1 = Customer(email='adam@demo.com', username='adam', password='password', postcode='ST34QX',house_number='99')'
#'volunteer_1 = Volunteer(email='brian@demo.com', username='brian', password='passwords', postcode='ST12NB', house_number='98', engaged=0)'
#'volunteer_2 = Volunteer(email='dave@demo.com', username='Dave', password='passwords1', postcode='ST32NB', house_number='100', engaged=0)'
#'product_1 = Products(name='bread', price='2.00') '
#'order_1 = Order(customer_id='1', volunteer_id='2', order_date='04042021', completed=0)'
#'db.session.add_all([customer_1, volunteer_1, volunteer_2, product_1, order_1])'
#'db.session.commit()'


#'0' is false and '1' is true in sql boolean data types.