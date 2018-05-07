# Generated by Django 2.0 on 2018-05-07 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20180507_0256'),
        ('people', '0010_auto_20180411_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='combatant',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='people_combatant_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='god',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='people_god_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='people_organization_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='people_person_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='race',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='people_race_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
    ]
