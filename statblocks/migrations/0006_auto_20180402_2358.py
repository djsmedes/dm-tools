# Generated by Django 2.0 on 2018-04-02 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statblocks', '0005_auto_20180402_2124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialproperty',
            options={'ordering': ['sort_priority']},
        ),
        migrations.AddField(
            model_name='specialproperty',
            name='sort_priority',
            field=models.IntegerField(default=0, help_text='Properties without a sort priority will come before those that have one. Higher numbers will sort lower.'),
        ),
    ]
