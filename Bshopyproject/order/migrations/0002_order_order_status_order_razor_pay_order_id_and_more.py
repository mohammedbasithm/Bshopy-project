# Generated by Django 4.2.1 on 2023-07-27 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'pending'), ('PAID', 'paid'), ('CANCELLED', 'cancelled'), ('DELIVERED', 'Delivered'), ('SHIPPED', 'Shipped'), ('RETURNED', 'Returned'), ('ORDERED', 'Ordered'), ('COMPLETED', 'Completed')], default='ordered', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_order_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_payment_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_payment_signature',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]