# Generated by Django 3.2.8 on 2022-09-29 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player_voice', '0003_remove_freshnews_imgs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freshnews',
            old_name='created',
            new_name='createdtime',
        ),
    ]
