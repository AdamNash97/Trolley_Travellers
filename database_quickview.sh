#! /bin/bash
function database_selector {

echo 'Which database table would you like to view?'
echo '1: Customer, 2: Volunteer, 3: Product, 4: Order'
read -p "Enter choice : " choice

if [ $choice = 1 ]
	then
table_var="Customer"
export table_var
table_query

elif [ $choice = 2 ]
	then
table_var="Volunteer"
export table_var
table_query

elif [ $choice = 3 ]
	then 
table_var="Product"
export table_var
table_query

elif [ $choice = 4 ]
	then 
table_var="Order"
export table_var
table_query

fi
echo 'Would you like to view another database table: [y, n]'
}

function table_query {
python << EOF
import os, importlib
table = os.environ['table_var']
print(table)
from trolleytravellers import db, create_app
app = create_app()
app.app_context().push()
from trolleytravellers.models import *
entities = eval(table).query.all()
for entity in entities:
	print(entity)
EOF
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

