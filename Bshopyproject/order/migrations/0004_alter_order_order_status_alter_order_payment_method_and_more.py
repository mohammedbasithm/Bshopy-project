# Generated by Django 4.2.1 on 2023-08-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_applied_coupon_order_cancelled_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('CANCELLED', 'cancelled'), ('DELIVERED', 'Delivered'), ('SHIPPED', 'Shipped'), ('RETURNED', 'Returned'), ('REQUEST FOR RETURN', 'request for return'), ('ORDERED', 'Ordered')], default='ordered', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('RAZORPAY', 'razorpay'), ('CASH_ON_DELIVERY', 'Cash on Delivery'), ('WALLET PAY', 'wallet pay')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('PAID', 'paid'), ('REFUNDED', 'refunded'), ('REFUND IN PROGRESS', 'refund in progress'), ('NO PAYMENT', 'no payment')], default='pending', max_length=25),
        ),
    ]
