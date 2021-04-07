from trolleytravellers import db, ma
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from enum import Enum

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
    engaged = db.Column(db.Boolean, nullable = False)
    # Defining one-to-many relationship: a volunteer can have several orders to fulfil (needs a function to delete completed orders)
    order = db.relationship("Order", backref="volunteer") # Specifying an additional argument `uselist=False` converts it into a 1-1 relationship

    def __init__(self, email, username, password, postcode, house_number, engaged):
        self.email = email
        self.username = username
        self.password = password
        self.postcode = postcode
        self.house_number = house_number
        self.engaged = engaged
    
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
        return f"Volunteer('{self.email}', '{self.username}', '{self.password}', '{self.postcode}', '{self.house_number}', '{self.engaged}')"


# Association table for many-to-many relationship to link left (order) table and right (product) table
class OrderProduct(db.Model):
    #__tablename__ = 'order_product'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable = False, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False, primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)
    # Defining relationship
    product = db.relationship("Product", backref="orders")

    def get_order_total(self):
        order_total = self.product.price * self.quantity
        return order_total

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        
    def __repr__(self):
        return f"Order('{self.order_id}', '{self.product_id}', '{self.quantity}')"

# not a table, rather it's for the enum data type below this class
class Status(Enum):
    PENDING = 1
    DISPATCHED = 2
    COMPLETED = 3

class Order(db.Model):
    #__tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.Integer, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'), nullable = True)
    status = db.Column(db.Enum(Status), nullable = False)
    # Defining relationship
    products = db.relationship("OrderProduct", backref="order")

    def __init__(self, order_date, customer_id, volunteer_id, status):
        self.order_date = order_date
        self.customer_id = customer_id
        self.volunteer_id = volunteer_id
        self.status = status

    def __repr__(self):
        return f"Order('{self.order_date}', '{self.customer_id}', '{self.volunteer_id}', '{self.status}')"

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

class OrderProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderProduct

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("order_date", "customer_id", "volunteer_id")
        
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product




customer_schema = CustomerSchema(many=True)
volunteer_schema = VolunteerSchema(many=True)
order_product_schema = OrderProductSchema(many=True)
order_schema = OrderSchema(many=True)
product_schema = ProductSchema(many=True)


