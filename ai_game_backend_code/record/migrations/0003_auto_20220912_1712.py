# Generated by Django 3.2.8 on 2022-09-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_auto_20220911_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='a_language',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='record',
            name='b_language',
            field=models.CharField(default='', max_length=20),
        ),
    ]
