# Generated by Django 4.2.1 on 2023-08-02 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0011_productvariant_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
