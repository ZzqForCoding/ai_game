# Generated by Django 3.2.8 on 2022-11-09 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_voice', '0006_auto_20221001_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='freshnews',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
