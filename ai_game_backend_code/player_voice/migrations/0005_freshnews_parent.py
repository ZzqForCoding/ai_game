# Generated by Django 3.2.8 on 2022-10-01 14:49

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('player_voice', '0004_rename_created_freshnews_createdtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='freshnews',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replyers', to='player_voice.freshnews'),
        ),
    ]
