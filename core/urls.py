from django.urls import path
from .views import product_list, cart_detail, add_to_cart,\
    remove_from_cart, clear_cart, checkout, checkout_success

urlpatterns = [
    path('', product_list, name='product_list'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout_success/', checkout_success, name='checkout_success'),
]
