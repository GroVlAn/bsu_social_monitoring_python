# Generated by Django 4.1.7 on 2023-04-21 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0033_organization_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
    ]
