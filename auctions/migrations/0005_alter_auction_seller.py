# Generated by Django 4.1.3 on 2022-11-20 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_bid_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gennarino', to=settings.AUTH_USER_MODEL),
        ),
    ]
