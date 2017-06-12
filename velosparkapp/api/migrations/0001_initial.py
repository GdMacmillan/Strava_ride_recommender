# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-11 23:48
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StravaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
            name='Activity',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('resource_state', models.PositiveSmallIntegerField()),
                ('external_id', models.CharField(max_length=140)),
                ('upload_id', models.IntegerField()),
                ('name', models.CharField(max_length=140)),
                ('distance', models.FloatField()),
                ('moving_time', models.DurationField()),
                ('elapsed_time', models.DurationField()),
                ('total_elevation_gain', models.FloatField()),
                ('type', models.CharField(max_length=140)),
                ('start_date', models.DateTimeField()),
                ('start_date_local', models.DateTimeField()),
                ('time_zone', models.CharField(max_length=140)),
                ('start_latlng', django.contrib.postgres.fields.jsonb.JSONField()),
                ('end_latlng', django.contrib.postgres.fields.jsonb.JSONField()),
                ('achievment_count', models.PositiveSmallIntegerField()),
                ('kudos_count', models.PositiveSmallIntegerField()),
                ('comment_count', models.PositiveSmallIntegerField()),
                ('athlete_count', models.PositiveSmallIntegerField()),
                ('photo_count', models.PositiveSmallIntegerField()),
                ('total_photo_count', models.PositiveSmallIntegerField()),
                ('trainer', models.BooleanField()),
                ('commute', models.BooleanField()),
                ('manual', models.BooleanField()),
                ('private', models.BooleanField()),
                ('flagged', models.BooleanField()),
                ('average_speed', models.FloatField()),
                ('max_speed', models.FloatField()),
                ('average_watts', models.FloatField()),
                ('max_watts', models.IntegerField()),
                ('weighted_average_watts', models.IntegerField()),
                ('kilojoules', models.FloatField()),
                ('device_watts', models.BooleanField()),
                ('has_heartrate', models.BooleanField()),
                ('average_heartrate', models.FloatField()),
                ('max_heartrate', models.PositiveSmallIntegerField()),
                ('calories', models.FloatField()),
                ('description', models.TextField()),
                ('suffer_score', models.PositiveSmallIntegerField()),
                ('has_kudoed', models.BooleanField()),
                ('segment_effort', django.contrib.postgres.fields.jsonb.JSONField()),
                ('splits_metric', django.contrib.postgres.fields.jsonb.JSONField()),
                ('laps', django.contrib.postgres.fields.jsonb.JSONField()),
                ('best_efforts', django.contrib.postgres.fields.jsonb.JSONField()),
                ('device_name', models.CharField(max_length=140)),
                ('embed_token', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('resource_state', models.PositiveSmallIntegerField()),
                ('firstname', models.CharField(max_length=140)),
                ('lastname', models.CharField(max_length=140)),
                ('profile_medium', models.SlugField()),
                ('profile', models.SlugField()),
                ('city', models.CharField(max_length=140)),
                ('state', models.CharField(max_length=140)),
                ('country', models.CharField(max_length=140)),
                ('sex', models.CharField(max_length=10)),
                ('friend', models.CharField(max_length=10)),
                ('follower', models.CharField(max_length=10)),
                ('premium', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('follower_count', models.PositiveSmallIntegerField()),
                ('friend_count', models.PositiveSmallIntegerField()),
                ('mutual_friend_count', models.PositiveSmallIntegerField()),
                ('athlete_type', models.PositiveSmallIntegerField()),
                ('date_preference', models.CharField(max_length=140)),
                ('measurement_preference', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=140)),
                ('ftp', models.PositiveSmallIntegerField()),
                ('weight', models.FloatField()),
                ('clubs', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bikes', django.contrib.postgres.fields.jsonb.JSONField()),
                ('shoes', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('summary_polyline', models.TextField()),
                ('resource_state', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Map'),
        ),
        migrations.AddField(
            model_name='activity',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Athlete'),
        ),
    ]
