#! /bin/bash

function database_selector {

echo 'Please select database table you would like to view?'
echo '1: Customer, 2: Volunteer, 3: Product'
read -p "Enter choice : " choice

if [ $choice = 1 ]
	then
python3 << EOF
from trolleytravellers import db, create_app
app = create_app()
app.app_context().push()
from trolleytravellers.models import Customer, Volunteer, Product
customers = Customer.query.all()
for customer in customers:
	print(customer)
EOF
elif [ $choice = 2 ]
	then
python3 << EOF
from trolleytravellers import db, create_app
app = create_app()
app.app_context().push()
from trolleytravellers.models import Customer, Volunteer, Product
volunteers = Volunteer.query.all()
for volunteer in volunteers:
	print(volunteer)
EOF
elif [ $choice = 3 ]
	then
python3 << EOF
from trolleytravellers import db, create_app
app = create_app()
app.app_context().push()
from trolleytravellers.models import Customer, Volunteer, Product
products = Product.query.all()
for product in products:
	print(product)
EOF
fi
echo 'Would you like to view another database table: [y, n]'
}

while :
do
	database_selector
read answer
if [ $answer = 'y' ]
  then 
  	database_selector
else 
   break
fi
done

