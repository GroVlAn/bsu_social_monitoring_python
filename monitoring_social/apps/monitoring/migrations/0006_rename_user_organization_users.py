# Generated by Django 4.1.7 on 2023-03-16 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0005_alter_organization_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='user',
            new_name='users',
        ),
    ]
