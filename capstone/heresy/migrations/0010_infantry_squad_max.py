# Generated by Django 4.1.7 on 2023-04-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heresy', '0009_remove_infantry_squad_max_infantry_squad_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='infantry',
            name='squad_max',
            field=models.IntegerField(default=5),
        ),
    ]
