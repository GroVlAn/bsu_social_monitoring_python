# Generated by Django 4.1.7 on 2023-05-09 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.TextField(verbose_name='UUID ссылки для приглашения')),
                ('user_id', models.IntegerField(verbose_name='ID пользователя')),
                ('team_id', models.IntegerField(verbose_name='ID команды')),
                ('date_create', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
