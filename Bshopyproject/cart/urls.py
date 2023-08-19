from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart,name='cart'),
    path('addcart/<int:selected_variant_id>/',views.add_to_cart,name='add-cart'),
    path('removecart',views.remove_from_cart,name='remove-cart'),
    path('wishlist/',views.wishlist,name='wish-list'),
    path('add-wishlist/<int:variant_id>/',views.add_to_wishlist,name='add-wishlist'),
    path('remove-wishlist/<int:variant_id>/',views.remove_wishlist,name='remove-wishlist'),
    path('update_quantity',views.update_quantity,name='update_quantity'),
    path('remove-coupon',views.remove_coupon,name='remove-coupon'),
]