# Generated by Django 4.1.7 on 2023-04-27 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0037_alter_organization_slug'),
        ('vk_api_app', '0008_rename_vkuserstatistic_vkuserstatistics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vksettings',
            name='user',
        ),
        migrations.AddField(
            model_name='vksettings',
            name='organization',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.organization'),
        ),
    ]
