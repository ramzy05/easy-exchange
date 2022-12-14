# Generated by Django 4.1 on 2022-09-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_alter_account_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='amount',
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount_in',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount_out',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(default='3365', max_length=4),
        ),
    ]
