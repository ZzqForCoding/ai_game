# Generated by Django 3.2.8 on 2022-11-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0027_alter_platformdata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformdata',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
