# Generated by Django 2.0.6 on 2018-07-28 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180728_0536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availability',
            old_name='ending_time',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='availability',
            old_name='starting_time',
            new_name='start_time',
        ),
    ]
