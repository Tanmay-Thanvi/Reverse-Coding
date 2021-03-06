# Generated by Django 4.0.2 on 2022-04-12 22:56

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_started', models.BooleanField(default=False)),
                ('is_notallowed', models.BooleanField(default=True)),
                ('StartTime', models.DateTimeField(blank=True, null=True)),
                ('ExpLgtTime', models.DateTimeField(blank=True, null=True)),
                ('CompTime', models.DateTimeField(blank=True, null=True)),
                ('Timetaken', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('zone', models.CharField(default='Red', max_length=100)),
                ('zone_activate', models.BooleanField(default=False)),
                ('riddle_activate', models.BooleanField(default=False)),
                ('teamwith', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
