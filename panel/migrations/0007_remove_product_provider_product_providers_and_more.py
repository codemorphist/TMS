# Generated by Django 5.2 on 2025-04-07 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_remove_product_provider_product_provider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='provider',
        ),
        migrations.AddField(
            model_name='product',
            name='providers',
            field=models.ManyToManyField(blank=True, related_name='providers', to='panel.provider'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='panel.productcategory'),
        ),
    ]
