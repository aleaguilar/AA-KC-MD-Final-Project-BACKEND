from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(80), nullable=False) #how to define the password column
    # order_history = relationship
    # search_history = relationship

    def __repr__(self):
        return '<Customer %r>' % self.name #make it a string?

    def serialize(self):
        return {
        "name": self.name,
        "lastname": self.lastname,
        "email": self.email,
        "address": self.address,
        "city": self.city,
        "country": self.country,
        "password": self.password
        }

class Queries(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amz_asin = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    upc = db.Column(db.String(25), nullable=False)
    customer_id = db.Column(db.String(25), nullable=False)
    
    def __repr__(self):
        return '<ASIN %r>' % self.amz_asin

    def serialize(self):
        return {
        "amz_asin": self.amz_asin,
        "price": self.price,
        "upc": self.upc,
        "user_id": self.user_id,
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_id = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    prod_name = db.Column(db.String(250), nullable=False)
    quantity = db.Column(db.Integer, nullable=False) #pull from front-end
    price = db.Column(db.Integer(), nullable=False)
    ship_cost = db.Column(db.Integer, nullable=False) #how and where to do the math
    ship_method = db.Column(db.String(25), nullable=False)
    order_total = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return '<Cart Total %r>' % self.order_total

    def serialize(self):
        return {
        "total": self.order_total,
        "shipping": self.ship_cost,
        "shipping method": self.ship_method,
        "id": self.order_temp_id,
        "quantity": self.quantity,
        "product": self.prod_name,
        }

class Orders(db.Model):
    id = db.Column(db.Integer, unique=True)
    order_num = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    subtotal = db.Column(db.Integer, nullable=False) 
    ship_amt = db.Column(db.Integer, nullable=False)
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

class Products(db.Model):
    id = db.Column(db.Integer, unique=True)
    prod_name = db.Column(db.String(250), nullable=False)
    amz_asin = db.Column(db.String(25), nullable=False, primary_key=True)
    last_price = db.Column(db.Integer(), nullable=False)
    upc = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    keywords = db.Column(db.String(250), nullable=False) #how to create an array for categories
    categories = db.Column(db.String(250), nullable=False) #how to create an array for categories
    fba = db.Column(db.Boolean(), nullable=True)
    prohibited = db.Column(db.Boolean(), nullable=True)
    ship_weight = db.Column(db.Integer, nullable=False) #how and where to do the math
    ocean_dimension = db.Column(db.Integer, nullable=False) #how and where to do the math
    air_dimension = db.Column(db.Integer, nullable=False) #how and where to do the math

    def __repr__(self):
        return '<Product %r>' % self.prod_name

    def serialize(self):
        return {
        "product name": self.prod_name,
        "description": self.description,
        "keywords": self.keywords,
        "categories": self.categories,
        "fba": self.fba,
        "prohibited": self.prohibited,
        "shipping weight": self.ship_weight,
        "ocean volume": self.ocean_dimension,
        "air volume": self.air_dimension,
        }

# class ProhibitedProducts(db.Model):
# class ShippingRates(db.Model):
