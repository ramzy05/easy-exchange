# Generated by Django 4.1 on 2022-09-01 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_remove_transaction_pin_account_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(default='0000', max_length=4),
        ),
    ]
