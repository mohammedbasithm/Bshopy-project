from django.db import models
from datetime import timedelta, timezone
from django.db import models
from userprofile.models import *
from django.utils import timezone
from Store.models import *
from cart.models import Coupon
# Create your models here.

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING','pending'),
        ('PAID','paid'),
        ('REFUNDED','refunded'),
        ('REFUND IN PROGRESS','refund in progress'),
        ('NO PAYMENT','no payment'),
    ]
    ORDER_STATUS_CHOICES = [
        ('CANCELLED','cancelled'),
        ('DELIVERED','Delivered'),
        ('SHIPPED','Shipped'),
        ('RETURNED','Returned'),
        ('REQUEST FOR RETURN','request for return'),
        ('ORDERED','Ordered'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('RAZORPAY', 'razorpay'),
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
        ('WALLET PAY','wallet pay'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('userprofile.UserAdress', on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_status = models.CharField(max_length=25, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)

    order_status=models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default='ordered',null=True,blank=True)
    razor_pay_order_id=models.CharField(max_length=150,null=True,blank=True)
    razor_pay_payment_id=models.CharField(max_length=150,null=True,blank=True)
    razor_pay_payment_signature=models.CharField(max_length=150,null=True,blank=True)

    shipping_charge=models.IntegerField(null=True)
    applied_coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    cancelled_date=models.DateTimeField(blank=True,null=True)
    returned_date=models.DateTimeField(blank=True,null=True)
    return_request_date=models.DateTimeField(blank=True,null=True)
    shipping_date=models.DateTimeField(blank=True,null=True)
    return_period_expired=models.DateTimeField(blank=True,null=True)


    def str(self):
        return f"{self.id, self.tracking_no}"
    def str(self):
        return f"{self.id}  {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_date:
            self.order_date = timezone.now()  # Set the order date to the current time if it's not set
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(hours=24)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    def str(self):
        return f"{self.order.id, self.order.tracking_no}"