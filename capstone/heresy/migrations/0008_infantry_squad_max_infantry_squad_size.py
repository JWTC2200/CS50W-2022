# Generated by Django 4.1.7 on 2023-04-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heresy', '0007_alter_infantry_options_infantry_inv_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='infantry',
            name='squad_max',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='infantry',
            name='squad_size',
            field=models.IntegerField(default=5),
        ),
    ]