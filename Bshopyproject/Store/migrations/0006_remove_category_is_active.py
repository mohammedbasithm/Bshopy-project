# Generated by Django 4.2.1 on 2023-07-24 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_alter_category_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_active',
        ),
    ]
