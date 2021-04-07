from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def main_message():
    return "Welcome to Trolley Travellers!"




