from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import *
from Store.models import *
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=50,unique=True,null=True)
    coupon_price=models.IntegerField(default=150)
    minimum_amount=models.IntegerField(default=750)
    is_expired=models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code

class UserCoupon(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE)
    used=models.BooleanField(default=False)
    total_price=models.BigIntegerField()

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_user_cart(sender, instance, created, **kwargs):
        if created:
            Cart.objects.create(user=instance)

    def __str__(self):
        return f"Cart{self.pk}for{self.user.username}"
    
    def get_total_price(self):
        return self.cartitems_set.aggregate(total_price=Sum('price'))['total_price']
    
class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quandity=models.PositiveBigIntegerField(default=1)
    price=models.DecimalField(max_digits=8,decimal_places=2)

    def get_item_price(self):
        return Decimal(self.price)*Decimal(self.quandity)
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user.username}"
    
class WishlistItem(models.Model):
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)

    def get_item_price(self):
        return self.product.price

    
    
        
    
