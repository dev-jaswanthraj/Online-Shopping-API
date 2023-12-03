from flask_restx import reqparse
from core import api

add_user_parser = reqparse.RequestParser()
add_user_parser.add_argument("username", type = str)
add_user_parser.add_argument("email", type = str)
add_user_parser.add_argument("password", type = str)

register_customer_parser = reqparse.RequestParser()
register_customer_parser.add_argument("address", type = str)
register_customer_parser.add_argument("phone", type = str)

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type = str)
login_parser.add_argument("password", type = str)

quantity_parser = reqparse.RequestParser()
quantity_parser.add_argument("quantity", type = int)