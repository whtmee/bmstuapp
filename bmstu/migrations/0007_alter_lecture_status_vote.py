# Generated by Django 5.2 on 2025-04-10 15:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu', '0006_balance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='status',
            field=models.CharField(choices=[('pending', 'На проверке'), ('approved', 'Принято'), ('rejected', 'Отклонено'), ('revision', 'На доработке')], default='pending', max_length=20, verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(verbose_name='Лайк')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('homework', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmstu.homework', verbose_name='Домашняя работа')),
                ('lecture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmstu.lecture', verbose_name='Лекция')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Голос',
                'verbose_name_plural': 'Голоса',
                'unique_together': {('user', 'homework'), ('user', 'lecture')},
            },
        ),
    ]
