# Generated by Django 3.2.8 on 2022-08-05 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('content', models.TextField(max_length=10000)),
                ('rating', models.IntegerField(default=1500)),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now)),
                ('modifytime', models.DateTimeField(auto_now=True)),
                ('game_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_bot', to='game.game')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bot', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
