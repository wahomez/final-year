# Generated by Django 4.1.7 on 2023-04-11 21:07

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('paid', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(default=datetime.datetime.now)),
                ('completed', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('pic', models.ImageField(upload_to='')),
                ('size', models.CharField(max_length=20)),
                ('store', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('trans_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('trans_type', models.CharField(choices=[('deposit', 'deposit'), ('payment', 'payment')], max_length=200, null=True)),
                ('recipient', models.CharField(max_length=200, null=True)),
                ('details', models.CharField(max_length=200, null=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.IntegerField()),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pic', models.ImageField(default='profile.png', null=True, upload_to='')),
                ('mobile_number', models.CharField(max_length=10, null=True)),
                ('location', models.CharField(choices=[('Nairobi', 'Nairobi'), ('Mombasa', 'Mombasa'), ('Mt Kenya', 'Mt Kenya')], max_length=200, null=True)),
                ('gas_brand', models.CharField(choices=[('K-gas', 'K-gas'), ('Total', 'Total'), ('Progas', 'Progas')], max_length=200, null=True)),
                ('gas_size', models.CharField(choices=[('6 kgs', '6 kgs'), ('13 kgs', '13 kgs')], max_length=20, null=True)),
                ('married', models.BooleanField(default=False, null=True)),
                ('household_number', models.IntegerField(null=True)),
                ('kids_number', models.IntegerField(default=0, null=True)),
                ('kids_below3', models.IntegerField(default=0, null=True)),
                ('cooking_sequence', models.IntegerField(null=True)),
                ('cooking_method', models.CharField(choices=[('Microwaving', 'Microwaving'), ('Stir-frying', 'Stir-frying'), ('Broiling', 'Broiling'), ('Steaming', 'Steaming'), ('Baking', 'Baking'), ('Roasting', 'Roasting'), ('Boiling', 'Boiling'), ('Simmering', 'Simmering')], max_length=200, null=True)),
                ('last_refill', models.DateField(null=True)),
                ('predicted_refill', models.DateField(null=True)),
                ('updated', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_order', to='base.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='base.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=200)),
                ('order_date', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('date_generated', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceb_product', to='base.product')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('delivery_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('delivery_point', models.CharField(max_length=200)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_order', to='base.order')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
