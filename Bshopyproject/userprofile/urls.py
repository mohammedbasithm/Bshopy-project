from . import views
from django.urls import path

urlpatterns = [
    path('userprofile/',views.user_profile,name='user-profile'),
    path('add-address',views.add_address,name='add-address'),
    path('show-address',views.show_address,name='show-address'),
    path('order-address',views.order_address,name='order-address'),
    path('delete-address/<int:address_id>',views.delete_address,name='delete-address'),
    path('no-address',views.no_address,name='no-address'),
    path('edit-address/<int:address_id>',views.edit_address,name='edit-address'),
    path('user-wallet',views.user_wallet,name='user-wallet'),
    path('edit-address-userside/<int:address_id>',views.edit_address_userside,name='edit-address-userside'),
]
