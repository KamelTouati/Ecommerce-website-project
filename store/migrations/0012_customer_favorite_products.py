# Generated by Django 4.1.6 on 2023-07-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_customer_options_alter_customer_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='favorite_products',
            field=models.ManyToManyField(to='store.product'),
        ),
    ]
