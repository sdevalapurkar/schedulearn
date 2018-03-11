# Generated by Django 2.0.3 on 2018-03-11 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationships',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_user_rel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relationships',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_user_rel', to=settings.AUTH_USER_MODEL),
        ),
    ]
