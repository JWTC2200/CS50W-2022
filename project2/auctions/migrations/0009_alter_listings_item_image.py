# Generated by Django 4.1.7 on 2023-03-18 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listings_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='item_image',
            field=models.URLField(blank=True, default=None, max_length=500, null=True),
        ),
    ]
