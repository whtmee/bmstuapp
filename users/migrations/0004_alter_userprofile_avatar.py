# Generated by Django 5.2 on 2025-04-11 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_userprofile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatars/default.png', upload_to='users_image/', verbose_name='Аватар'),
        ),
    ]
