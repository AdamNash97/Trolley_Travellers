from trolleytravellers import create_app
#Call create app function
app = create_app()
#Run application directly using python without environment variables:
#Can now run just using: 'python run.py'
if __name__ == '__main__':
    app.run(debug=True)
#To activate the v_env:
#'. ./trolleytravellers_env/Scripts/activate'

#To write a requirements.txt  with all required dependencies:
#'pip install pipreqs'
#'pipreqs /path/to/project'