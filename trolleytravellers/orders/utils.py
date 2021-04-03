from trolleytravellers import db
from trolleytravellers.models import Customer, Volunteer
import re
from sqlalchemy import create_engine

#Need to fix this later, but will work fine now in order to create cursor for database.
engine = create_engine('sqlite:///site.db')
connection = engine.raw_connection()
c = connection.cursor()

#Will likely use in order utils also, eventually!
global customer_postcode_first_half 

#Function to be called upon posting of Order request (submission of order).
def find_volunteer_match(customer):
    #Must pass current customer's details, hence must be logged in.
    current_customer = Customer.query.get(customer.id)
    customer_postcode = current_customer.postcode
    #Delete any spaces and convert to upper case.
    postcode_to_process = customer_postcode.replace(" ","").upper()
    #Regex to extract all components of postcode, regardless of length, for UK postcodes.
    postcode_components = re.findall(r'^((([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,2})) {0,}(([0-9])([A-Z]{2})))', postcode_to_process)
    #Extract just first half postcode from customer:
    customer_postcode_first_half = postcode_components[1]
    
    volunteer_postcodes_first_halves = []
    volunteer_ids = []
    #Take id and postcode columns from volunteer table.
    c.execute('SELECT id, postcode FROM volunteer') 
    for volunteer in c:
        current_vol_postcode = c[volunteer].postcode
        current_vol_postcode  = current_vol_postcode.replace(" ","").upper()
        postcode_comps = re.findall(r'^((([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,2})) {0,}(([0-9])([A-Z]{2})))', current_vol_postcode)
        #Store volunteer's id and first half of postcode in a dictionary:
        volunteer_postcodes_first_halves.append(postcode_comps[1])
        volunteer_ids.append(c[volunteer].id)
    
    #Loop over list of first half of volunteer postcodes to look for a match with
    #customer's first half of postcode:
    looper = 0
    for row in volunteer_postcodes_first_halves:
        while looper==0:
            #When first match is found, exit while loop and record the row of the matched volunteer
            if volunteer_postcodes_first_halves[row] == customer_postcode_first_half:
                looper=1
                matched_volunteer_row=row

    #Find the id of the matched volunteer by accessing the relevant row in the list of volunteer ids stored.
    matched_volunteer_id = volunteer_ids[matched_volunteer_row]
    
    #Query the volunteer database to get all the details of the matched volunteer.
    matched_volunteer = Volunteer.query.get(matched_volunteer_id)
    
    return matched_volunteer
   

    #Alternative, definitely easier option, for finding matched customer (found after all the effort made for the above):
    #postcode_matches = db.execute('SELECT id, email, username, postcode FROM volunteer WHERE postcode=customer_postcode')