# Generated by Django 4.2.2 on 2023-07-26 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_remove_category_is_active'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together=set(),
        ),
    ]
