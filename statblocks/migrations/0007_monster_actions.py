# Generated by Django 2.0 on 2018-04-03 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statblocks', '0006_auto_20180402_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='actions',
            field=models.ManyToManyField(blank=True, to='statblocks.Action'),
        ),
    ]
