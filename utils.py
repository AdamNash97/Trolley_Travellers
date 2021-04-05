from sqlalchemy import create_engine
from trolleytravellers import db, create_app
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import re

app = create_app()
app.app_context().push()


engine = create_engine('sqlite:///site.db', echo=True)
from trolleytravellers.models import Customer, Volunteer, Order
Session = sessionmaker(bind=engine)

session = Session()
sql = text('select username from customers')
result = db.engine.execute(sql)
usernames = [row[1] for row in result]





session.commit()
session.close()
