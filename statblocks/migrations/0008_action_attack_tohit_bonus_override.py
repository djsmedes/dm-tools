# Generated by Django 2.0 on 2018-04-03 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statblocks', '0007_monster_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='attack_tohit_bonus_override',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
