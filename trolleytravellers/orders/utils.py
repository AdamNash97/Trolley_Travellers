from trolleytravellers.models import Customer
import re, sqlite3
from sqlite3 import Error
from flask import request
import json

database = r"./trolleytravellers/site.db"

#General method to be used for creating a connection to the database
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

#Will likely use in order utils also, eventually!
global customer_postcode_first_half 

#Function to be called upon posting of Order request (submission of order).
def find_volunteer_match(customer_id):
    #Must pass current customer's details, hence must be logged in.
    current_customer = Customer.query.get(customer_id)
    customer_postcode = current_customer.postcode
    #Delete any spaces and convert to upper case.
    postcode_to_process = customer_postcode.replace(" ","").upper()
    #Regex to extract all components of postcode, regardless of length, for UK postcodes.
    postcode_components = re.findall(r'^((([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,2})) {0,}(([0-9])([A-Z]{2})))', postcode_to_process)
    #Extract just first half postcode from customer:
    customer_postcode_first_half = postcode_components[0][1]
    #Calculate length of postcode extraction
    len_postcode = len(customer_postcode_first_half)
    #create_connection(database)
    create_connection(database)
    cur = conn.cursor()
    #Take id and postcode columns from volunteer table.
    cur.execute(f"SELECT id, substr(postcode, 1, {len_postcode}), engaged FROM volunteer;") 
    rows = cur.fetchall()
    for row in rows:
        #If postcode matches and the volunteer is not currently engaged (FALSE=0 in SQL boolean types)
        if row[1] == customer_postcode_first_half and row[2] == 0:
            matched_volunteer_id = int(row[0])
            break
    #Close connection to database
    conn.close()
    return matched_volunteer_id

#Deviated away from WHERE and LIKE sql keyword idea since LIKE means we're not doing an exact match 
#(postcode = value), but doing some more fuzzy matching. "%" is a wildcard character - 
#it matches 0 or more characters in the passed customer postcode, so this is saying 
#"all rows where the column has 0 or more chars followed by "mystring" followed by 0 or more chars".
#This might not be accurate with longer and more varied postcodes that have similar components.


def create_shopping_list():
 
    product_names = request.json['product_names']
    conn = create_connection(database)
    cur = conn.cursor()
    shopping_list, initial_shopping_list = [], []
    cur.execute("SELECT id, name FROM product")
    product_rows = cur.fetchall()

    all_items = {} 
    for product in product_rows:
        all_items[product[1]] = str(product[0]) # dictionary (product name: product id)

    # appends product ids to initial_shopping_list via dictionary
    for product in product_names:
        if product in all_items:
            initial_shopping_list.append(all_items[str(product)]) 
            
    # One column list of product ids, perform counting, deletion and quantity variables
    shopping_list = [ [product, initial_shopping_list.count(product)] for product 
    in list(set(initial_shopping_list)) ] # [ [product, quantity], [product, quantity], ...,
                                          # [product, quantity] ]
    conn.close()

    return shopping_list

