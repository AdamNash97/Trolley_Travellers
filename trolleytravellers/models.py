from trolleytravellers import db, ma 

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

    def __init__(self, order=None):
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
    # quantity = db.Column(db.Integer) # Assuming unlimited stock for MVP

    def __init__(self,price, name, quantity):
        self.price = price
        self.name = name
        # self.quantity = quantity # Assuming unlimited stock for MVP

    def info(self):
        return {
            'id': self.id,
            'price': self.price,
            'name': self.name,
            # 'quantity': self.quantity, # Assuming unlimited stock for MVP
        }
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.info())


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


