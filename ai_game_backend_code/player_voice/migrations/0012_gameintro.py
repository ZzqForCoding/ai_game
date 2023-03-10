# Generated by Django 3.2.8 on 2022-11-19 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('player_voice', '0011_auto_20221118_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameIntro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, max_length=20000, null=True)),
                ('createdtime', models.DateTimeField(auto_now_add=True)),
                ('is_post', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
