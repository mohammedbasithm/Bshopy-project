# Generated by Django 4.2.1 on 2023-08-02 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_alter_product_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
