# Generated by Django 3.2.8 on 2022-09-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_remove_player_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='openid',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
