# Generated by Django 2.2.3 on 2019-09-07 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('feed_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('cast', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=20)),
                ('language', models.CharField(choices=[('ENGLISH', 'English'), ('BENGALI', 'Bengali'), ('HINDI', 'Hindi'), ('TAMIL', 'Tamil'), ('TELUGU', 'Telugu'), ('MALAYALAM', 'Malayalam'), ('MARATHI', 'Marathi'), ('FRENCH', 'French')], max_length=10)),
                ('run_length', models.IntegerField(help_text='Enter run length in minutes')),
                ('certificate', models.CharField(choices=[('U', 'U'), ('UA', 'U/A'), ('A', 'A'), ('R', 'R')], max_length=2)),
                ('popularity_index', models.IntegerField(blank=True, null=True, unique=True)),
                ('trailer', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_no', models.BigIntegerField()),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Theatre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(choices=[('DELHI', 'Delhi'), ('KOLKATA', 'Kolkata'), ('MUMBAI', 'Mumbai'), ('CHENNAI', 'Chennai'), ('BANGALORE', 'Bangalore'), ('HYDERABAD', 'Hyderabad')], max_length=9)),
                ('address', models.CharField(max_length=30)),
                ('no_of_screen', models.IntegerField()),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.Movie')),
                ('theatre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.Theatre')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=3)),
                ('seat_type', models.CharField(choices=[('', 'Select'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum')], max_length=8)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Show')),
            ],
            options={
                'unique_together': {('no', 'show')},
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%S')),
                ('payment_type', models.CharField(choices=[('Debit Card', 'Debit Card'), ('Credit Card', 'Credit Card'), ('Net Banking', 'Net Banking'), ('Wallet', 'Wallet')], max_length=11)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='add_movies',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('cast', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=10)),
                ('run_length', models.IntegerField(help_text='Enter run length in minutes')),
                ('screen_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('trailer', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('time', models.CharField(max_length=30)),
                ('movie_desc', models.CharField(max_length=500)),
            ],
            options={
                'unique_together': {('time', 'screen_id')},
            },
        ),
        migrations.CreateModel(
            name='BookedSeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Booking')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Seat')),
            ],
            options={
                'unique_together': {('seat', 'booking')},
            },
        ),
    ]
