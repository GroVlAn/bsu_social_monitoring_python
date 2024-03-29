# Generated by Django 4.1.7 on 2023-03-30 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0022_rename_reports_analyseditemssummarystatistics_reposts_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnalysedItemsSummaryStatistics',
            new_name='AnalyzedItemsSummaryStatistics',
        ),
        migrations.CreateModel(
            name='AnalyzedItemKeyWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.analyzeditem')),
            ],
        ),
    ]
