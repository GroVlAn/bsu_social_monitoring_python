# Generated by Django 4.1.7 on 2023-04-02 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vk_api_app', '0005_vkignoreusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='VkUserSummaryStatistics',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='vk_user_summary', serialize=False, to='vk_api_app.vkuser')),
                ('score', models.IntegerField()),
            ],
            options={
                'db_table': 'vk_user_summary_statistics',
            },
        ),
        migrations.RemoveField(
            model_name='vkuser',
            name='statistics',
        ),
        migrations.AddField(
            model_name='vkuserstatistic',
            name='date_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vkuserstatistic',
            name='date_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vkuserstatistic',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vk_api_app.vkuser'),
        ),
        migrations.AlterModelTable(
            name='vkuserstatistic',
            table='vk_user_statistic',
        ),
    ]
