from flask_jwt_extended import get_jwt_identity
from core.models import (
    User,
    Customer, 
)


def get_customer_details():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(email = user_identity).first()
    customer = Customer.query.filter_by(user_id = user.id).first()

    return customer