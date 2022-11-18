# Generated by Django 3.2.8 on 2022-11-09 22:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('player_voice', '0007_freshnews_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='freshnews',
            name='players',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]