# Generated by Django 4.1.7 on 2023-05-09 23:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_invitation_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='UUID',
            field=models.TextField(default=uuid.uuid4, editable=False, verbose_name='UUID ссылки для приглашения'),
        ),
    ]
