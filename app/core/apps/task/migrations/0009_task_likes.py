# Generated by Django 5.0.6 on 2024-07-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_browhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='likes',
            field=models.BigIntegerField(default=0),
        ),
    ]
