# Generated by Django 4.1 on 2022-09-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0007_alter_account_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(default='0123', max_length=4),
        ),
    ]
