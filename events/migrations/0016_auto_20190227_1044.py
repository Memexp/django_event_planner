# Generated by Django 2.1.7 on 2019-02-27 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follwer',
            new_name='f',
        ),
    ]
