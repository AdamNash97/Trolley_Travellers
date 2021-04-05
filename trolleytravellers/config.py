
#Combine all configuration in a single object to allow inheritance later.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

#Create database and add data in terminal:
#'python'
#'from trolleytravellers import db, create_app'
#'app = create_app()'
#'app.app_context().push()'
#'from trolleytravellers.models import Customer, Volunteer, Order, Products, Order_Products'
#'db.create_all()'
#'customer_1 = Customer(email='adam@demo.com', username='adam', password='password', postcode='ST34QX',house_number='99')'
#'volunteer_1 = Volunteer(email='brian@demo.com', username='brian', password='passwords', postcode='ST12NB', house_number='98', engaged=0)'
#'volunteer_2 = Volunteer(email='dave@demo.com', username='Dave', password='passwords1', postcode='ST32NB', house_number='100', engaged=0)'
#'product_1 = Products(name='bread', price='2.00') '
#'order_1 = Order(customer_id='1', volunteer_id='2', order_date='04042021', completed=0)'
#'db.session.add_all([customer_1, volunteer_1, volunteer_2, product_1, order_1])'
#'db.session.commit()'


#'0' is false and '1' is true in sql boolean data types.