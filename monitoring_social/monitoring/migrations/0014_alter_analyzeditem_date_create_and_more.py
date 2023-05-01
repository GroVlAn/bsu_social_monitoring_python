# Generated by Django 4.1.7 on 2023-03-17 11:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0013_analyzeditem_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyzeditem',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='analyzeditem',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]