# Generated by Django 3.2.8 on 2022-09-12 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0011_player_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='token',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]