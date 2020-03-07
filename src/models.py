from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(80), nullable=False) #how to define the password column
    cod_lib = db.Column(db.String(15), nullable=True)
    # order_history = relationship
    # search_history = relationship

    def __repr__(self):
        return '<Customer %r>' % self.name #make it a string?

    def serialize(self):
        return {
        "name": self.name,
        "lastname": self.lastname,
        "email": self.email,
        "phone": self.phone,
        "address": self.address,
        "city": self.city,
        "country": self.country,
        "cod_lib": self.cod_lib,
        }

class Queries(db.Model):
    id = db.Column(db.Integer, unique=True)
    session_id = db.Column(db.Integer, primary_key=True, unique=True) #how to define session duration and how to use date format plus numbers
    date = db.Column(db.DateTime, nullable=False)
    amz_asin = db.Column(db.String(25), nullable=False)
    upc = db.Column(db.String(25), nullable=False)
    product = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    keywords = db.Column(db.String(250), nullable=False) #how to create an array for categories
    categories = db.Column(db.String(250), nullable=False) #how to create an array for categories
    fba = db.Column(db.Boolean(), nullable=True)
    prohibited = db.Column(db.Boolean(), nullable=True)
    ship_weight = db.Column(db.Integer, nullable=False) #how and where to do the math
    ocean_dimension = db.Column(db.Integer, nullable=False) #how and where to do the math
    air_dimension = db.Column(db.Integer, nullable=False) #how and where to do the math
    added_cart = db.Column(db.Boolean(), nullable=True)
    last_added_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return '<Search %r>' % self.order_num

    def serialize(self):
        return {
        "product": self.product,
        "description": self.description,
        "price": self.price,
        "fba": self.fba,
        "prohibited": self.prohibited,
        "weight": self.ship_weight,
        "cubic_feet": self.ocean_dimension,
        "volumetric": self.air_dimension,
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_temp_id = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    prod_name = db.Column(db.String(250), nullable=False)
    quantity = db.Column(db.Integer, nullable=False) #pull from front-end
    price = db.Column(db.Integer(), nullable=False)
    ship_cost = db.Column(db.Integer, nullable=False) #how and where to do the math
    order_total = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return '<Cart Total %r>' % self.order_total

    def serialize(self):
        return {
        "total": self.order_total,
        "id": self.order_temp_id,
        "quantity": self.quantity,
        "product": self.prod_name,
        }

class Orders(db.Model):
    id = db.Column(db.Integer, unique=True)
    order_num = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    subtotal = db.Column(db.Integer(), nullable=False) 
    ship_amt = db.Column(db.Integer(), nullable=False)
    ship_method = db.Column(db.String(25), nullable=False)
    status = db.Column(db.String(15), nullable=True)
    receiver_code = db.Column(db.String(15), nullable=False)


    def __repr__(self):
        return '<Order %r>' % self.order_num

    def serialize(self):
        return {
        "order": self.order_num,
        "customer": self.customer_id,
        "date": self.date,
        "total": self.subtotal,
        "shipping": self.ship_amt,
        "method": self.ship_method,
        "status": self.status,
        "receiver": self.receiver_code,
        }

