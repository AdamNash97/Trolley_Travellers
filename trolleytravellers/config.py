#Combine all configuration in a single class to allow inheritance later when app is created.
class Config:
    #Link to database stored locally
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #For production, should ideally store in an environment variable locally and use os package to access the secret key: 
    SECRET_KEY = '7e9d2cb1f691ff74c8862c62df1502b6'
    #Configuration values needed for mail server setup:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    #TLS: Transport Layer Security - Cryptographic protocols for communication security over computer network.
    MAIL_USE_TLS = True
    #Ideally should also store the username and password below on your local machine as environment variables for security reasons.
    #That would be done in the following way:
    #MAIL_USERNAME = os.environ.get('EMAIL_TT')
    #MAIL_PASSWORD = os.environ.get('PASS_TT')
    MAIL_USERNAME = 'trolleytravellers@gmail.com'
    MAIL_PASSWORD = 'Trolleys2021'

#Generating the secret key used above:
#In python terminal:
#'import secrets'
#'secrets.token_hex(16)'

#Create the database called site.db from scratch by following the steps below in the terminal:
#'python'
#'from trolleytravellers import db, create_app'
#'app = create_app()'
#'app.app_context().push()'
#'from trolleytravellers.models import Customer, Volunteer, Order, Product, OrderProduct'
#'db.create_all()'
