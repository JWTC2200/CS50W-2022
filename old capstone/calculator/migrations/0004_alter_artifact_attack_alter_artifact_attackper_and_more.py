# Generated by Django 4.1.7 on 2023-04-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_weapons_user_weapons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='attack',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='attackper',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='base_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_anemo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_cryo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_dendro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_electro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_geo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_hydro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_physical',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='bonus_pyro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='crit_damage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='crit_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='defence',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='defenceper',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='elemental_mastery',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='energy_recharge',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='healing_bonus',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='health',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='healthper',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='artifact_set',
            name='bonus_value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]