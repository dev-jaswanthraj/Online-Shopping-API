from core import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(12))
    customer = db.relationship('Customer', backref = 'user')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order = db.relationship('Order', backref = 'customer')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    type = db.Column(db.String(200))
    price = db.Column(db.Float)
    order = db.relationship('OrderDetail', backref = 'product')

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, default = 1)
    order = db.relationship("Order", backref = "order_detail")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default = datetime.today())
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    order_detail_id = db.Column(db.Integer, db.ForeignKey('order_detail.id'))
    payment_status = db.Column(db.Boolean, default = False)
    subtotal = db.Column(db.Float)

class Payment(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default = datetime.today())
    orders = db.Column(db.String(500))
