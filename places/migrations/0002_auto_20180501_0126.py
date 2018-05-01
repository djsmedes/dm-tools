# Generated by Django 2.0 on 2018-05-01 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ['_dimensions']},
        ),
        migrations.AddField(
            model_name='place',
            name='_dimensions',
            field=models.IntegerField(blank=True, choices=[(0, 'point'), (1, 'line'), (2, 'polygon')], db_column='dimensions', null=True),
        ),
    ]
