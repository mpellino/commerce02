# Generated by Django 4.1.3 on 2022-11-19 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
