# Generated by Django 4.2.1 on 2023-07-31 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_alter_productimage_variant'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'brand_name')},
        ),
    ]
