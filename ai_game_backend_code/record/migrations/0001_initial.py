# Generated by Django 3.2.8 on 2022-08-20 17:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_id', models.IntegerField()),
                ('a_sx', models.IntegerField()),
                ('a_sy', models.IntegerField()),
                ('b_id', models.IntegerField()),
                ('b_sx', models.IntegerField()),
                ('b_sy', models.IntegerField()),
                ('a_steps', models.TextField(max_length=1000)),
                ('b_steps', models.TextField(max_length=1000)),
                ('map', models.TextField(max_length=1000)),
                ('loser', models.CharField(max_length=10)),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_record', to='game.game')),
            ],
        ),
    ]