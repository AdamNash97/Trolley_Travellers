from trolleytravellers import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), unique = True, nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    housenumber = db.Column(db.String(4), nullable = False)
    orders = db.relationship("Order", back_populates="customers")


class Volunteer(db.Model):
    __tablename__ = 'volunteer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), unique = True, nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    housenumber = db.Column(db.String(4), nullable = False)
    customers_order_id = db.Column(db.Integer(4), db.ForeignKey('shoppinglist'))

    orders = db.relationship("ShoppingList", back_populates="volunteers")


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    orderdate = db.Column(db.Integer)
    customer_postcode = db.Column(db.String)
    customers = db.relationship("Customer", back_populates="orders")

    shoppinglists = db.relationship("ShoppingList", back_populates="orders2shop")


class ShoppingList(db.Model):
    __tablename__ = 'shoppinglist'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))
    orderdate = db.Column(db.Integer)
    items = db.relationship("Product")
    volunteers = db.relationship("Volunteer", back_populates="orders")

    orders2shop = db.relationship("Order", back_populates="shoppinglists")
    

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    supermarket_id = db.Column(db.String, db.ForeignKey('supermarket.id'))
    category = db.Column(db.String)
    price = db.Column(db.Integer)
    status = db.Column(db.String)
    

class Supermarket(db.Model):
    __tablename__ = 'supermarket'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    postcode = db.Column(db.String)
