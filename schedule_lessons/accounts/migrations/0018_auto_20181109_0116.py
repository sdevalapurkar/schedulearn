# Generated by Django 2.0.6 on 2018-11-09 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20181109_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link_one',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AddField(
            model_name='notification',
            name='link_three',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AddField(
            model_name='notification',
            name='link_two',
            field=models.CharField(default='', max_length=60),
        ),
    ]