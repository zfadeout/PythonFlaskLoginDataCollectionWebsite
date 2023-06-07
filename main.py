#Importing from init.py create app
from website import create_app

app = create_app()

#To run the flask application
if __name__ == '__main__':
    app.run(debug=True)