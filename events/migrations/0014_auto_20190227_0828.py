# Generated by Django 2.1.7 on 2019-02-27 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_event_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashbord',
            name='event',
        ),
        migrations.RemoveField(
            model_name='dashbord',
            name='user',
        ),
        migrations.DeleteModel(
            name='Dashbord',
        ),
    ]