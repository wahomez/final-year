# Generated by Django 4.1.5 on 2023-03-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='last_refillspan',
        ),
        migrations.AddField(
            model_name='profile',
            name='last_refill',
            field=models.DateField(null=True),
        ),
    ]