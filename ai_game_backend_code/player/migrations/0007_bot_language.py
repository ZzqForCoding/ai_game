# Generated by Django 3.2.8 on 2022-09-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20220822_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='language',
            field=models.CharField(default='cpp', max_length=10),
        ),
    ]
