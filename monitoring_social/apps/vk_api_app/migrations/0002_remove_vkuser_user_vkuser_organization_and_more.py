# Generated by Django 4.1.7 on 2023-03-27 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0020_alter_groupanalyzeditems_organization'),
        ('vk_api_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkuser',
            name='user',
        ),
        migrations.AddField(
            model_name='vkuser',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.organization'),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='first_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='last_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
