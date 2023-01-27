from flask import Flask, request, jsonify, make_response 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_migrate import Migrate

load_dotenv()

PSQL_USER_ENV=os.getenv('PSQL_USER')
PSQL_PWD_ENV=os.getenv('PSQL_PWD')
PSQL_URI_ENV=os.getenv('PSQL_URI')
PSQL_PORT_ENV=os.getenv('PSQL_PORT')
PSQL_DB_NAME_ENV=os.getenv('PSQL_DB_NAME')

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/flask_test'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation
        
    def __repr__(self):
        return '<Product %d>' % self.id
    
    
class AuthorSchema(ma.Schema):
    class Meta:
        model = Author
        sqla_session = db.session
        
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)
    
    def __repr__(self):
        return '<Product %d>' % self.id
    
with app.app_context():    
    db.create_all()
    
@app.before_request
def before_request():
    print(request.method, request.endpoint)
    
@app.route('/authors', methods = ['GET'])
def index():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['id', 'name', 'specialisation'])
    authorr, error = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authorr}))  

@app.route('/authors', methods = ['POST'])
def create_author():
  data = request.get_json()
  author_schema = AuthorSchema()
  authorr, error = author_schema.load(data)
  print(f'authors: {type(authorr)}, {authorr}, data {data}')
  result = author_schema.dump(authorr.create()).data
  return make_response(jsonify({"author": result}),200)  


if __name__ == '__main__':
    app.run(debug=True)