from django.urls import path
from userprofile import views
from . import views


urlpatterns = [

    path('check-out/<int:adres_id>',views.check_out,name='check-out'),
    path('order-placed/<int:order_id>',views.place_order,name='place-order'),
    path('wallet-pay/<int:order_id>',views.pay_wallet,name='pay-wallet'),
    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('online_payment_order/<add_id>',views.online_payment_order,name='online_payment_order'),
    path('order-success',views.order_success,name='order-success'),
    path('order-list',views.order,name='order'),
    path('order-view/<int:order_id>',views.order_view,name='order-view'),
    path('order-cancel/<int:order_id>',views.order_cancel,name='order-cancel'),
    path('order-return/<int:order_id>',views.return_request,name='order-return'),
    
]