# Generated by Django 3.2.8 on 2022-09-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0004_auto_20220912_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='a_sx',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='a_sy',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='b_sx',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='b_sy',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='map',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
