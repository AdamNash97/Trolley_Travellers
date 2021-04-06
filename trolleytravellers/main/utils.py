from datetime import datetime

#Used to access current date for order_date attribute

def get_current_date():
    # Creating a datetime object so we can test.
    current_date = datetime.now()
    # Converting a to string in the desired format (YYYYMMDD) using strftime
    # and then to int.
    current_date = int(current_date.strftime('%Y%m%d'))
    return current_date