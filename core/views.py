from core import db, api
from flask_restx import Resource, marshal
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from core.parsers import (
    add_user_parser,
    register_customer_parser,
    login_parser,
    quantity_parser
)
from core.models import (
    User,
    Customer, 
    Product, 
    Order,
    OrderDetail,
    Payment
)
from core.seralizer import (
    user_resource,
    customer_resource,
    product_resource,
    cart_resource
)
from core.utils import (
    get_customer_details,
)

class UserAdd(Resource):
    @api.expect(add_user_parser)
    def post(self):
        req_data = add_user_parser.parse_args()
        user_check = User.query.filter_by(email = req_data['email']).first()
        if user_check:
            return {'msg': 'User Email Alreay Exists.'}, 409
        user = User(
            username = req_data['username'],
            email = req_data['email'],
            password = req_data['password']
        )
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_resource), 201

class Login(Resource):
    @api.expect(login_parser)
    def post(self):
        req_data = login_parser.parse_args()
        user = User.query.filter_by(email = req_data['email']).first()
        if user:
            if user.password == req_data['password']:
                return {'Token': 'Bearer {}'.format(create_access_token(identity=req_data['email'])), 'user': marshal(user, user_resource)}, 200
            else:
                return {'msg': 'email or password is invalid.'}, 404
        else:
            return {'msg': 'email or password is invalid.'}, 404
        
class CustomerRegister(Resource):
    @jwt_required()
    @api.expect(register_customer_parser)
    @api.header('Authorization', 'Bearer Token')
    def post(self):
        req_data = register_customer_parser.parse_args()
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email = user_identity).first()
        customer = Customer.query.filter_by(user_id = user.id).first()

        if None in req_data.values():
            return {'msg': 'All Fields should be filled.'}, 400
        
        if customer:
            return {'msg': 'User Data Already Created.'}, 409
        
        customer_data = Customer(
            address = req_data['address'],
            phone = req_data["phone"],
            user_id = user.id
        )

        db.session.add(customer_data)
        db.session.commit()

        return marshal(customer_data, customer_resource), 201

    @jwt_required()
    @api.expect(register_customer_parser)
    @api.header('Authorization', 'Bearer Token')
    def patch(self):
        req_data = register_customer_parser.parse_args()
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email = user_identity).first()
        customer_data = Customer.query.filter_by(user_id = user.id).first()

        if customer_data == None:
            return {'msg': 'User Data Not Found.'}, 404
        
        customer_data.address = req_data['address'] if req_data['address'] != None else customer_data.address
        customer_data.phone = req_data['phone'] if req_data['phone'] != None else customer_data.phone

        db.session.commit()

        return marshal(customer_data, customer_resource), 200

    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    def delete(self):
        req_data = register_customer_parser.parse_args()
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email = user_identity).first()
        customer_data = Customer.query.filter_by(user_id = user.id).first()

        if customer_data == None:
            return {'msg': 'User Data Not Found.'}, 404
        
        db.session.delete(customer_data)
        db.session.commit()

        return {"msg": "Successfuly Deleted."}, 200
    
class ProductList(Resource):
    def get(self):
        product_data = Product.query.all()
        return marshal(product_data, product_resource), 200

class ShoppingCart(Resource):
    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    def get(self):
        customer = get_customer_details()
        if customer == None:
            return {'msg': 'Please Add Address and Phone Number.'}, 404
        order_data = Order.query.filter_by(customer_id = customer.id, payment_status = False).all()
        return marshal(order_data, cart_resource), 200
        
class AddToCart(Resource):
    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    def post(self, id):
        customer = get_customer_details()
        if customer == None:
            return {'msg': 'Please Add Address and Phone Number.'}, 404
        product = db.session.get(Product, id)
        if product == None:
            return {'msg': 'Product Not Found.'}, 404
        order_details = OrderDetail.query.filter_by(product_id = product.id).all()
        check = None
        for order_detail in order_details:
            check = Order.query.filter_by(order_detail_id = order_detail.id, payment_status = False, customer_id = customer.id).first()
            break
        if check:
            order_detail.quantity += 1
            check.subtotal = order_detail.quantity * product.price
            db.session.commit()

            return marshal(check, cart_resource), 201
        
        order_detail = OrderDetail(
            product_id = product.id,
        )
        db.session.add(order_detail)
        db.session.commit()
        order = Order(
            customer_id = customer.id,
            subtotal = order_detail.quantity * product.price,
            order_detail_id = order_detail.id
        )
        db.session.add(order)
        db.session.commit()
        return marshal(order, cart_resource), 201

    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    @api.expect(quantity_parser)
    def patch(self, id):
        customer = get_customer_details()
        if customer == None:
            return {'msg': 'Please Add Address and Phone Number.'}, 404
        product = db.session.get(Product, id)
        if product == None:
            return {'msg': 'Product Not Found.'}, 404
        req_data = quantity_parser.parse_args()
        if req_data['quantity'] < 1:
            return {'msg': 'Quantity Should be >= 1'}, 409
        order_details = OrderDetail.query.filter_by(product_id = product.id).all()
        check = None
        for order_detail in order_details:
            check = Order.query.filter_by(order_detail_id = order_detail.id, payment_status = False, customer_id = customer.id).first()
            break
        if check:
            order_detail.quantity = req_data['quantity']
            check.subtotal = order_detail.quantity * product.price
            db.session.commit()
            return marshal(check, cart_resource), 201
        return {'msg': "Product not in Cart."}, 404
    
    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    def delete(self, id):
        customer = get_customer_details()
        if customer == None:
            return {'msg': 'Please Add Address and Phone Number.'}, 404
        product = db.session.get(Product, id)
        if product == None:
            return {'msg': 'Product Not Found.'}, 404
        order_details = OrderDetail.query.filter_by(product_id = product.id).all()
        check = None
        for order_detail in order_details:
            check = Order.query.filter_by(order_detail_id = order_detail.id, payment_status = False, customer_id = customer.id).first()
            break
        if check:
            db.session.delete(order_detail)
            db.session.delete(check)
            db.session.commit()
            return marshal(check, cart_resource), 201
        return {'msg': "Product not in Cart."}, 404

class PaymentGateway(Resource):
    @jwt_required()
    @api.header('Authorization', 'Bearer Token')
    def post(self):
        customer = get_customer_details()
        orders = Order.query.filter_by(payment_status = False, customer_id = customer.id).all()
        if len(orders) == 0:
            return {'msg': "No Product Found in Cart."}, 409
        amount = 0
        order_ids = []
        for order in orders:
            amount += order.subtotal
            order_ids.append(str(order.id))
            order.payment_status = True
        payment = Payment(
            amount = amount,
            orders = " | ".join(order_ids)
        )
        db.session.add(payment)
        db.session.commit()
        return {'msg': 'Payment Done'}, 200
        