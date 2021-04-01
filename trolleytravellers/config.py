
#Combine all configuration in a single object to allow inheritance later.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

#Create database in terminal:
#'python'
#'from trolleytravellers import db, create_app'
#'db.create_all(app=create_app())'
#The above code creates a 'site.db' in the trolleytravellers package.
#We can add all tables to this one database.

#Start by importing all models in models.py (not done yet), then add all data manually. 
#Run the following code in the terminal to do so:
#The code blow is just an example of creating a customer in the database.
#WE NEED TO DISCUSS THE ORDERS ATTRIBUTE ON CUSTOMER CLASS, NOT SURE IT WILL WORK!
#'from trolleytravellers import Customer, Volunteer, Order, ShoppingList, Product, Supermarket'
#'customer_1 = Customer(email='adam@demo.com', username='adam', password='password', postcode='ST34QX',housenumber='99', orders=[])'
#'db.session.add(customer_1)'
#Now commit the changes to the database:
#'db.session.commit()'
