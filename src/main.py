"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Customer, Queries, Products, Orders, Cart
from activecampaign.client import Client
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

#from models import Person

client = Client('https://libertyexpress.api-us1.com', os.environ.get('AC_KEY'))
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'  # Change this!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
@jwt_required
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/customers', methods=['GET'])
def handle_customers():
    print("something")
    all_customers = Customer.query.all()
    all_customers = list(map(lambda x: x.serialize(), all_customers))
    return jsonify(all_customers), 200

@app.route('/register', methods=['POST'])
def registration():

    new_user = request.get_json()
    print("new_user",new_user)

    if 'name' not in new_user:
        raise APIException ("Hey, we need to know who to deliver this to. Tell us your name", status_code=400)
    
    if 'lastname' not in new_user:
        raise APIException ("We need your lastname too", status_code=400)
    
    if 'email' not in new_user:
        raise APIException ("Email is always required!", status_code=400)

    if 'address' not in new_user:
        raise APIException ("You want your package, right? We need an address for that", status_code=400)

    if 'password' not in new_user:
        raise APIException ("Please set a password", status_code=400)
    
    user1 = Customer(name=new_user['name'], lastname=new_user['lastname'], email=new_user['email'], address=new_user['address'], city=new_user['city'], country=new_user['country'], password=new_user['password'])
    print("user1", user1)
    db.session.add(user1)
    db.session.commit()

    return jsonify({'message':"User Successfully Created"}), 200


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Please provide email"}), 400
    if not password:
        return jsonify({"msg": "Please provide a password"}), 400

    boboo =  Customer.query.filter_by(email=email, password=password).first()
    if boboo == None:
         return jsonify({"msg": "Bad boboo or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email),"name":boboo.name}
    return jsonify(ret), 200


# Protect a view with jwt_required, which requires a valid jwt
# to be present in the headers.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200

if __name__ == '__main__':
    app.run()

@app.route('/subscribe', methods=['POST'])
def email_subscriber():

    body = request.get_json()

    response = client.contacts.create_a_contact(body)    

    return jsonify({'message':"Contact added"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)