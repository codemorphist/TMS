# Generated by Django 5.2 on 2025-04-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
