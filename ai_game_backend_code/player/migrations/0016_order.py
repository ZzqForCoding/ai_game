# Generated by Django 3.2.8 on 2022-11-11 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('player', '0015_remove_player_is_expand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_id', models.CharField(max_length=100)),
                ('out_trade_no', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('finish_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]