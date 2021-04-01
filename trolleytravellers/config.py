
#Combine all configuration in a single object to allow inheritance later.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

#Create databases in terminal
# sqlite3 site.db
# .tables
#.exit
