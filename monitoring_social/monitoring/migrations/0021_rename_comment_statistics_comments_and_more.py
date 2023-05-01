# Generated by Django 4.1.7 on 2023-03-29 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0020_alter_groupanalyzeditems_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='comment',
            new_name='comments',
        ),
        migrations.AddField(
            model_name='statistics',
            name='date_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='statistics',
            name='date_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]