# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "<h1>Home Page</h1>"

# if __name__ == '__main__':
#     app.run(debug=True)

from trolleytravellers import create_app
#Call create app function
app = create_app()
#Run application directly using python without environment variables:
#Can now run just using: 'python run.py'
if __name__ == '__main__':
    app.run(debug=True)
