# Generated by Django 4.1.7 on 2023-04-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0027_groupanalyzeditems_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupanalyzeditems',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]