# Generated by Django 4.1.6 on 2023-03-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='User',
            new_name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]