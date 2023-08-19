from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('men/',views.men,name='men'),
    path('category/<slug:slug>/',views.category,name='category'),
    # path('productdetails/<slug:slug>/', views.product, name='product'),
    # path('productdetails/<slug:slug>/',views.product,name='product'),
    path('productdetails/<slug:slug>', views.productdetails, name='productdetails'),
    path('get-variant/',views.get_variant,name='get-variant'),
    path('shop',views.shop,name='shop'),



]