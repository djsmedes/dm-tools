# Generated by Django 2.0 on 2018-04-03 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statblocks', '0009_auto_20180403_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='specific_to_monster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unique_actions', to='statblocks.Monster'),
        ),
    ]
