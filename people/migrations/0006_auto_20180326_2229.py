# Generated by Django 2.0 on 2018-03-26 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20180326_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='god',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'npc', 'verbose_name_plural': 'npcs'},
        ),
        migrations.AlterModelOptions(
            name='population',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='god',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='organizations_in',
            field=models.ManyToManyField(blank=True, related_name='members', to='people.Organization'),
        ),
        migrations.AlterField(
            model_name='person',
            name='populations_in',
            field=models.ManyToManyField(blank=True, related_name='members', to='people.Population'),
        ),
        migrations.AlterField(
            model_name='person',
            name='race',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members_of_race', to='people.Population'),
        ),
    ]
