# Generated by Django 5.2 on 2025-04-09 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
    ]
