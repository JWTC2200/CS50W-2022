# Generated by Django 4.1.7 on 2023-03-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='item_image',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
