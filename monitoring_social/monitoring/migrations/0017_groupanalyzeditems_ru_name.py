# Generated by Django 4.1.7 on 2023-03-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0016_alter_groupanalyzeditems_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupanalyzeditems',
            name='ru_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Русское имя группы элементов'),
        ),
    ]
