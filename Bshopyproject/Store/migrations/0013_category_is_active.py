# Generated by Django 4.2.1 on 2023-08-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0012_alter_productvariant_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
