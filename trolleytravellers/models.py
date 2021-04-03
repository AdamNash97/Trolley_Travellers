from trolleytravellers import db, ma

class Customer(db.Model):
    #__tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    house_number = db.Column(db.String(4), nullable = False)

    def __init__(self, email, username, password, postcode, house_number):
        self.email = email
        self.username = username
        self.password = password
        self.postcode = postcode
        self.house_number = house_number 

class Volunteer(db.Model):
    #__tablename__ = 'volunteer'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    username = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)
    postcode = db.Column(db.String(40), nullable = False)
    house_number = db.Column(db.String(4), nullable = False)

    def __init__(self, email, username, password, postcode, house_number):
        self.email = email
        self.username = username
        self.password = password
        self.postcode = postcode
        self.house_number = house_number 

class Order(db.Model):
    #__tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    order = db.Column(db.String(1000))
    order_date = db.Column(db.Integer, nullable = False)
    customer_house_number = db.Column(db.Integer, db.ForeignKey('customer.house_number'))
    customer_postcode = db.Column(db.String(40), db.ForeignKey("customer.postcode"))

    def __init__(self, order=None):
        self.order = order

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

# Initalisation of Schema
customer_schema = CustomerSchema(many=True)
volunteer_schema = VolunteerSchema(many=True)
#Orders_schema = OrderSchema(many=True)

# # require initialisation for either scenario i.e. if single product is wanted by geriatric or greater than one product. 
# Order_schema = OrderSchema(strict=True)
# Orders_schema = OrdersSchema(strict=True)


# class ShoppingListSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = ShoppingList

# class ProductSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Product

# class SupermarketSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Supermarket



