# Generated by Django 4.1.7 on 2023-04-04 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0029_alter_analyzeditemssummarystatistics_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupanalyzeditems',
            name='name',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='Группа элементов'),
        ),
    ]
