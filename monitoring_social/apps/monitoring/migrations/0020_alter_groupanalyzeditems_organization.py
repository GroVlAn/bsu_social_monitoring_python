# Generated by Django 4.1.7 on 2023-03-25 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0019_remove_groupanalyzeditems_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupanalyzeditems',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.organization'),
        ),
    ]