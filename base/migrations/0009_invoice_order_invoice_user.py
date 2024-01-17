# Generated by Django 4.1.7 on 2023-04-12 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_saving_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_order', to='base.order'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice', to=settings.AUTH_USER_MODEL),
        ),
    ]
