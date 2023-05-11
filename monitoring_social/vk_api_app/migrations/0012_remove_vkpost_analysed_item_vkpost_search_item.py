# Generated by Django 4.1.7 on 2023-05-11 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0039_rename_groupanalyzeditems_groupsearchitems_and_more'),
        ('vk_api_app', '0011_rename_organization_vkignoreusers_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkpost',
            name='analysed_item',
        ),
        migrations.AddField(
            model_name='vkpost',
            name='search_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.searchitem'),
        ),
    ]
