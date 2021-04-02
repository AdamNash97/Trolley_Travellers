from trolleytravellers import db, ma

#JOHNNYS CODE###################################################################
# class Customer(db.Model):
#     __tablename__ = 'customer'
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(80), unique = True, nullable = False)
#     username = db.Column(db.String(40), unique = True, nullable = False)
#     password = db.Column(db.String(40), unique = True, nullable = False)
#     postcode = db.Column(db.String(40), nullable = False)
#     housenumber = db.Column(db.String(4), nullable = False)
#     # Pseudo-column
#     orders = db.relationship("Order", back_populates="customer")


# class Volunteer(db.Model):
#     __tablename__ = 'volunteer'
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(80), unique = True, nullable = False)
#     username = db.Column(db.String(40), unique = True, nullable = False)
#     password = db.Column(db.String(40), unique = True, nullable = False)
#     postcode = db.Column(db.String(40), nullable = False)
#     housenumber = db.Column(db.String(4), nullable = False)
#     # Pseudo-column
#     shoppinglists = db.relationship("ShoppingList", back_populates="volunteer")


# class Order(db.Model):
#     __tablename__ = 'order'
#     id = db.Column(db.Integer, primary_key = True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
#     orderdate = db.Column(db.Integer)
#     customer_postcode = db.Column(db.String)
#     # Pseudo-columns
#     customers = db.relationship("Customer", back_populates="order")
#     shoppinglists = db.relationship("ShoppingList", back_populates="order")


# class ShoppingList(db.Model):
#     __tablename__ = 'shoppinglist'
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     quantity = db.Column(db.Integer)
#     # Pseudo-columns
#     volunteers = db.relationship("Volunteer", back_populates="shoppinglist")
#     orders = db.relationship("Order", back_populates="shoppinglist")
#     products = db.relationship("Product", back_populates="shoppinglist")
    

# class Product(db.Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)
#     supermarket_id = db.Column(db.String, db.ForeignKey('supermarket.id'))
#     category = db.Column(db.String)
#     price = db.Column(db.Integer)
#     status = db.Column(db.String)
#     # Pseudo-columns
#     shoppinglists = db.relationship("ShoppingList", back_populates="product")
#     supermarkets = db.relationship("Supermarket", back_populates="product")

    
# class Supermarket(db.Model):
#     __tablename__ = 'supermarket'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String)
#     postcode = db.Column(db.String)
#     # Pseudo-column
#     supermarkets = db.relationship("Product", back_populates="supermarket")

#OZANS CODE#######################################################################
class Customer(db.Model):
    #__tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    housenumber = db.Column(db.String(4), nullable = False)
    order_list = db.Column(db.String(1000), nullable = True)
    # order = db.relationship("Order", foreign_keys='Order.order')

class Volunteer(db.Model):
    #__tablename__ = 'volunteer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    housenumber = db.Column(db.String(4), nullable = False)

    customer_housenumber = db.Column(db.Integer, db.ForeignKey('customer.housenumber'))
    customer_postcode = db.Column(db.String(40), db.ForeignKey("customer.postcode"))
    customer_order_list = db.Column(db.String(1000), db.ForeignKey('customer.order_list'))
    customer_order_date = db.Column(db.String(40), db.ForeignKey("order.order_date"))  

class Order(db.Model):
    #__tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    order = db.Column(db.String(1000))
    order_date = db.Column(db.Integer, nullable = False)
    customer_housenumber = db.Column(db.Integer, db.ForeignKey('customer.housenumber'))
    customer_postcode = db.Column(db.String(40), db.ForeignKey("customer.postcode"))

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

# class ShoppingListSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = ShoppingList

# class ProductSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Product

# class SupermarketSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Supermarket


