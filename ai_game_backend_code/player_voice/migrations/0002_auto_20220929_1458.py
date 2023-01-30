# Generated by Django 3.2.8 on 2022-09-29 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('player_voice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freshnews',
            name='player',
        ),
        migrations.AddField(
            model_name='freshnews',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_freshnews', to=settings.AUTH_USER_MODEL),
        ),
    ]