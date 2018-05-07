# Generated by Django 2.0 on 2018-05-07 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_campaign_current_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='base_campaign_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dmscreentab',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='base_dmscreentab_owned_set', to='base.Profile'),
            preserve_default=False,
        ),
    ]
