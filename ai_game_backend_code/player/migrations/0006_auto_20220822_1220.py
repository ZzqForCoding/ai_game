# Generated by Django 3.2.8 on 2022-08-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20220806_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bot',
            name='rating',
        ),
        migrations.AddField(
            model_name='player',
            name='rating',
            field=models.IntegerField(default=1500),
        ),
    ]
