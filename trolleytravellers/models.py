from trolleytravellers import db, ma
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Customer(db.Model):
    #__tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    house_number = db.Column(db.String(4), nullable = False)
    # Defining one-to-many relationship: a customer submits several orders 
    orders = db.relationship("Order", backref="customer") # backref puts a property "customer" on the "Order" class

    def __init__(self, email, username, password, postcode, house_number):
        self.email = email
        self.username = username
        self.password = password
        self.postcode = postcode
        self.house_number = house_number 

    #Create a password reset token that lasts for 30 minutes.
    def get_reset_token(self, expires_sec=1800):
        #Creates serializer.
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        #Pass in current user id as payload. Return token.
        return s.dumps({'customer_id': self.id}).decode('utf-8')

    #Doesn't do anything with instance of user, doesn't use self variable, so needs
    #to be declared as a static method. Will verify token created in function above.
    @staticmethod
    def verify_reset_token(token):
        #Creates serializer.
        s = Serializer(current_app.config['SECRET_KEY'])
        #Token could be expired or invalid if after 30 mins, so use a try-catch block.
        try:
            customer_id = s.loads(token)['customer_id']
        except:
            return None
        #Return customer with customer id if successful.
        return Customer.query.get(customer_id)

    def __repr__(self):
        return f"Customer('{self.email}', '{self.username}', '{self.password}', '{self.postcode}', '{self.house_number}')"

class Volunteer(db.Model):
    #__tablename__ = 'volunteer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    house_number = db.Column(db.String(4), nullable = False)
    # Defining one-to-one relationship: a volunteer has only one order to fulfil at one time
    orders = db.relationship("Order", backref="volunteer", uselist=False) # Specifying uselist=False converts it into a 1-1 relationship

    def __init__(self, email, username, password, postcode, house_number):
        self.email = email
        self.username = username
        self.password = password
        self.postcode = postcode
        self.house_number = house_number 
    
     #Create a password reset token that lasts for 30 minutes.
    def get_reset_token(self, expires_sec=1800):
        #Creates serializer.
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        #Pass in current user id as payload. Return token.
        return s.dumps({'volunteer_id': self.id}).decode('utf-8')

    #Doesn't do anything with instance of user, doesn't use self variable, so needs
    #to be declared as a static method. Will verify token created in function above.
    @staticmethod
    def verify_reset_token(token):
        #Creates serializer.
        s = Serializer(current_app.config['SECRET_KEY'])
        #Token could be expired or invalid if after 30 mins, so use a try-catch block.
        try:
            volunteer_id = s.loads(token)['volunteer_id']
        except:
            return None
        #Return customer with customer id if successful.
        return Volunteer.query.get(volunteer_id)

    def __repr__(self):
        return f"Volunteer('{self.email}', '{self.username}', '{self.password}', '{self.postcode}', '{self.house_number}')"

# Association table for many-to-many relationship: An order has a list of products to shop, and a product can be referenced more than once in several orders
intermediary = db.Table('intermediary',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Order(db.Model):
    #__tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.Integer, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable = False)
    # Defining many-to-many relationship
    shoppinglists = db.relationship("Product", secondary=intermediary, backref="orders")

    def __init__(self, order_date, customer_id, volunteer_id):
        self.order_date = order_date
        self.customer_id = customer_id
        self.volunteer_id = volunteer_id

    def __repr__(self):
        return f"Order('{self.order_date}', '{self.customer_id}', '{self.volunteer_id}')"

class Product(db.Model):
    #__tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(80))

    def __init__(self, price, name):
        self.price = price
        self.name = name

    def __repr__(self):
        return f"Product('{self.price}', '{self.name}')"



#SCHEMA################################################################ 
#Create Marshmallow Schema (JSON Serialisable objects that are a mixture of python dictionaries and lists)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class VolunteerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Volunteer

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Initalisation of Schema
customer_schema = CustomerSchema(many=True)
volunteer_schema = VolunteerSchema(many=True)
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema(many=True)


