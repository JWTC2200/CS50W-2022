# Generated by Django 4.1.7 on 2023-04-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heresy', '0004_weapons_effects'),
    ]

    operations = [
        migrations.AddField(
            model_name='infantry',
            name='member_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='infantry',
            name='unit_cost',
            field=models.IntegerField(default=0),
        ),
    ]
