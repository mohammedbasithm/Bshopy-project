from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order

# Create your models here.
class UserAdress(models.Model):
    user    =models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.EmailField(max_length=254)
    phone_number=models.CharField(max_length=14)
    address_line1=models.CharField(max_length=250)
    address_line2=models.CharField(max_length=250,blank=True,null=True)
    post_code=models.CharField(max_length=10)
    city=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    country=models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.first_name},{self.email},{self.state}"
    
class Wallet(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.balance}"
    
       
@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE,blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=(
        ('PURCHASE', 'Purchase'),
        ('CANCEL', 'Cancel'),
        ('RETURN', 'Return'),
    ))

    def _str_(self):
        return f"Wallet Transaction: {self.amount} - {self.date}"