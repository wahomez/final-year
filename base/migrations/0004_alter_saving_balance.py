# Generated by Django 4.1.7 on 2023-04-11 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='balance',
            field=models.FloatField(),
        ),
    ]