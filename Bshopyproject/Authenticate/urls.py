from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('',views.home,name='home'),
    path('signout',views.signout,name='signout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path('verification-mail-sent/',views.verification_mail_sent,name='verification_mail_sent'),
    path('otp_login',views.otp_login,name='otp-login'),
    path('password_reset/', views.password_reset_request, name='password-reset-request'),
    path('verify_otp/', views.verify_otp, name='verify-otp'),
    path('reset_password/', views.reset_password, name='reset-password'),

]