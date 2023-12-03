from core.views import (
    UserAdd,
    CustomerRegister,
    Login,
    ProductList, 
    ShoppingCart,
    AddToCart,
    PaymentGateway
)
from core import api

api.add_resource(UserAdd, "/user/add")
api.add_resource(CustomerRegister, "/customer/register")
api.add_resource(Login, "/user/login")
api.add_resource(ProductList, "/product/all")
api.add_resource(ShoppingCart, '/shoppingcart/all')
api.add_resource(AddToCart, '/addtocart/<int:id>')
api.add_resource(PaymentGateway, '/payment')