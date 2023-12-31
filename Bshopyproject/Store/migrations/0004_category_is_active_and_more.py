# Generated by Django 4.2.1 on 2023-07-24 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_productvariant_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'size')},
        ),
    ]
