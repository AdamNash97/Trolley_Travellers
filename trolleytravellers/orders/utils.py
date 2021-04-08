from trolleytravellers.models import Customer
import re, sqlite3
from sqlite3 import Error
from flask import request

database = r"./trolleytravellers/site.db"

# General method to be used for creating a connection to the database
def create_connection(database):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    global conn 
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn

# Variable needs to be access using global scope
global customer_postcode_first_half 

# Function to be called upon posting of Order request (submission of order).
def find_volunteer_match(customer_id):
    # Must pass current customer's details, hence must be logged in.
    current_customer = Customer.query.get(customer_id)
    customer_postcode = current_customer.postcode
    # Delete any spaces and convert to upper case.
    postcode_to_process = customer_postcode.replace(" ","").upper()
    # Regex to extract all components of postcode, regardless of length, for UK postcodes.
    postcode_components = re.findall(r'^((([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,2})) {0,}(([0-9])([A-Z]{2})))', postcode_to_process)
    # Extract just first half postcode from customer:
    customer_postcode_first_half = postcode_components[0][1]
    # Calculate length of postcode extraction
    len_postcode = len(customer_postcode_first_half)
    create_connection(database)
    cur = conn.cursor()
    # Take id and postcode columns from volunteer table.
    cur.execute(f"SELECT id, substr(postcode, 1, {len_postcode}), engaged FROM volunteer;") 
    rows = cur.fetchall()
    
    #Default value of 0, since the databse index starts at 1 and hence volunteer 0 doesn't exist.
    matched_volunteer_id = 0
    for row in rows:
        # If postcode matches and the volunteer is not currently engaged (FALSE=0 in SQL boolean types):
        if row[1] == customer_postcode_first_half and row[2] == 0:
            matched_volunteer_id = int(row[0])
            break
    # Close connection to database
    conn.close()
    
    return matched_volunteer_id

def create_shopping_list():
    product_names = request.json['product_names']
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM product")
    product_rows = cur.fetchall() 
    # returns list of lists
    # [ [product_id, product_name, product_price], ..., [product_id, product_name, product_price] ]

    all_items = {} 
    for product in product_rows:
        all_items[product[1]] = str(product[0]) # dictionary (product name: product id)
        all_items[str(product[0])] = float(product[2]) # dictionary (product id: price)
    # appends product ids to initial_shopping_list via dictionary

    shopping_list, initial_shopping_list, initial_customer_shopping_list  = [], [], []
    for product in product_names:
        if product in all_items:
            initial_shopping_list.append(all_items[str(product)]) # appends product ids to initial shopping list
            initial_customer_shopping_list.append(str(product)) # appends product names to initial shopping list
            
    sum_of_shopping_list = 0 # initialise empty variable to increment
    for item in initial_shopping_list:
        sum_of_shopping_list += all_items[str(item)] # use product_id : price key : value pairs to increment sum
            
    shopping_list = [ [product, initial_shopping_list.count(product)] for product 
                    in list(set(initial_shopping_list)) ] 
                    # [ [product, quantity], ..., [product, quantity] ]
    customer_shopping_list = [ [ product, initial_customer_shopping_list.count(product) ] for product
    in list(set( initial_customer_shopping_list)) ] # [ [ product_name, quantity ] ... ]
    conn.close()
    list_of_shopping_lists = [ shopping_list, customer_shopping_list, sum_of_shopping_list ]
    # list of lists which are lists of lists to be used in orders route to create an order.
    return list_of_shopping_lists

