# Generated by Django 4.1.7 on 2023-04-02 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vk_api_app', '0007_alter_vkuserstatistic_owner'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VkUserStatistic',
            new_name='VkUserStatistics',
        ),
    ]
