# Generated by Django 3.2.8 on 2022-11-22 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0026_platformdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformdata',
            name='date',
            field=models.CharField(max_length=30),
        ),
    ]