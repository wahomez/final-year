# Generated by Django 4.1.7 on 2023-04-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_saving_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='balance',
            field=models.CharField(max_length=200),
        ),
    ]
