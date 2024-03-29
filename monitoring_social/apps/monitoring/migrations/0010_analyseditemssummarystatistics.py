# Generated by Django 4.1.7 on 2023-03-17 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_alter_analyzeditem_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysedItemsSummaryStatistics',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='monitoring.analyzeditem')),
                ('likes', models.TextField(default=0)),
                ('comment', models.TextField(default=0)),
                ('reports', models.TextField(default=0)),
                ('score', models.TextField(default=0)),
            ],
            options={
                'db_table': 'monitoring_analyzed_items_summary_statistics',
            },
        ),
    ]
