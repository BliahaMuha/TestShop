from django.urls import path
from .views import remove_from_cart, ProductListView, checkout_success,\
    ClearCartView, checkout, add_to_cart, cart_detail


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('checkout_success/', checkout_success, name='checkout_success'),
]
