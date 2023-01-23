from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

PSQL_USER_ENV=os.getenv('PSQL_USER')
PSQL_PWD_ENV=os.getenv('PSQL_PWD')
PSQL_URI_ENV=os.getenv('PSQL_URI')
PSQL_PORT_ENV=os.getenv('PSQL_PORT')
PSQL_DB_NAME_ENV=os.getenv('PSQL_DB_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/flask_test'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    
    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation
    def __repr__(self):
        return '<Product %d>' % self.id
    
with app.app_context():    
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)