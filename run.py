from trolleytravellers import create_app
#Call create_app function in run.py
app = create_app()
#Run application directly using python without environment variables:
#Can now run app just using: 'python run.py'
if __name__ == '__main__':
    app.run(debug=True)


#To write a requirements.txt with all required dependencies:
#'pip install pipreqs'
#'pipreqs /path/to/project'