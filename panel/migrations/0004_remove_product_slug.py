# Generated by Django 5.2 on 2025-04-06 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
