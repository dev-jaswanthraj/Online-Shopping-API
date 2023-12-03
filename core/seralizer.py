from flask_restx import fields
from core.models import OrderDetail

user_resource = {
    'username': fields.String,
    'email': fields.String,
    'id': fields.Integer
}

customer_resource = {
    'id': fields.Integer,
    'address': fields.String,
    'phone': fields.String,
    'user': fields.Nested(user_resource)
}

product_resource = {
    'id': fields.Integer,
    'name': fields.String,
    'type':  fields.String,
    'price': fields.Float
}


order_detail_resource = {
    'id': fields.Integer,
    'product': fields.Nested(product_resource),
    'quantity': fields.Integer
}

cart_resource = {
    'id': fields.Integer,
    'order_detail': fields.Nested(order_detail_resource),
    'payment_status': fields.Boolean,
    'subtotal': fields.Float,
    'date': fields.DateTime
}