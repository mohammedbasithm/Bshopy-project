# Generated by Django 4.2.1 on 2023-07-24 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_category_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
