# Generated by Django 2.0.6 on 2019-03-06 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20181103_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
