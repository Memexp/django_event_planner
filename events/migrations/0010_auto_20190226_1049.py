# Generated by Django 2.1.7 on 2019-02-26 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='starting_time',
        ),
    ]
