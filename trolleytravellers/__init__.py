from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from trolleytravellers.config import Config
from flask_bcrypt import Bcrypt

#Create instance of database
db = SQLAlchemy()

#Create instance of marshmallow for schema
ma = Marshmallow()

#Initialise Bcrypt for hashing passwords for database storage
bcrypt = Bcrypt()

def create_app(config_class=Config):

    #name is the name of the current python module
    app = Flask(__name__)
    #Linking to config.py file to set configurations
    app.config.from_object(Config)

    #use init_app to pass in app to extension initialisation
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    
    from trolleytravellers.main.routes import main
    from trolleytravellers.user_customer.routes import user_customer
    from trolleytravellers.user_volunteer.routes import user_volunteer
    from trolleytravellers.products.routes import products
    from trolleytravellers.orders.routes import orders
    from trolleytravellers.errors.error_handlers import errors

    #Register blueprints
    app.register_blueprint(orders)
    app.register_blueprint(user_customer)
    app.register_blueprint(user_volunteer)
    app.register_blueprint(products)
    app.register_blueprint(main)
    app.register_blueprint(errors)
   
    return app


    