# Generated by Django 4.1.7 on 2023-03-28 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_api_app', '0003_alter_vkuser_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='id_user',
            field=models.IntegerField(unique=True),
        ),
    ]