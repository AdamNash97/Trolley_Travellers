# Trolley_Travellers
<img width="770" alt="Screenshot 2021-04-02 at 01 32 46" src="https://user-images.githubusercontent.com/68763259/113367236-6a4e0a00-9353-11eb-9884-10c337f224e2.png">

To run the Trolley_Travellers backend application, please clone to your local machine and open in a python ide of your choice. Then, in your terminal, please run the following the following commands, assuming you already have pip installed:

1) 'pip install -r requirements.txt' -> This will install all the package dependencies contained within the project globally on your computer. You can add '--save' to the end of this command if you wish to only install the packages in the project directory. Otherwise, feel free to run a virtual environment.
2) 'python run.py' -> This will start the local server that will be used to access the routes written within our application.

Once you have started the server, we recommend installing PostmanCanary (https://www.postman.com/downloads/canary/) and using it to test out the Trolley_Travellers REST API. Once you have the desktop version installed, you can add a new collection, and then add requests to that collection that pass in the URLs associated with each route we have written within our application. (see Postman website for instructions)

To do this successfully, please ensure that your 'Body' is set to 'raw' and the 'type' set to 'JSON'. Then simply follow the instructions below to test out the most important URL routes in our application (Copy and Paste in each part to the Postman app):

1) Request: GET
   URL: http://127.0.0.1:5000/customer_login
   Body: [{"username" : "johngerman","password" : "iJ0P3v9yHi6K"}]
   
2) Request: POST
   URL: http://127.0.0.1:5000/create_shopping_list
   Body: {"customer_id" : "53", "product_names": ["Yucca", "Rhubarb","Yucca"]}
   
3) Request: POST
   URL: http://127.0.0.1:5000/place_order_and_find_volunteer
   Body: {"customer_id" : "53", "product_names": ["Yucca", "Rhubarb","Yucca"]}
   
3) Request: POST
   URL: http://127.0.0.1:5000/order_completed
   Body: {"order_id" : "11"}
   
4) Request: PUT
   URL: http://127.0.0.1:5000/order_cancelled
   [{"order_id" : "2", "token" : "eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNzg5MTE0NSwiZXhwIjoxNjE3ODkxNzQ1fQ.eyJjdXN0b21lcl9pZCI6NTN9.Zs2c6hyhxI4m7pVK-nd0OXFiscOCHr7z526ZQZbeJX_tbYf4_xiBHfg9b3hsaDLw03DhWFfbY2DD6Wci37X9XA"}]
   
5) Request: PUT
   URL: http://127.0.0.1:5000/order_completed
   Body: {"order_id" : "11"}
   
**NOTE: For route 4 above to run successfully, you must first use route 3 and then copy and paste the 'token' returned in the JSON output into the body you pass into route 4. The token has a 2-hour expiry time after route 3 is run.
For all other CRUD operations, please see the routes.py files associated with each of our packages. 
FYI: You may have to change the 'order_id' etc. passed in the body depending on what is currently in the database. The best ways to do this would be to run the shell script in our repo, or use a SQL database browser to see what exists. For example, you can't query on order 12 if there are only 10 orders in the database.

To run the shell script, in your terminal, please run:
1) 'chmod +x database_quickview.sh'
2) './database_quickview.sh'
Note: You may have to change the interpreter variable in the file from 'python3' to 'python' in order to gain permission to run the script if you only have one version of python specified on you PATH variable, as opposed to many copies (python 2,3 etc.)



