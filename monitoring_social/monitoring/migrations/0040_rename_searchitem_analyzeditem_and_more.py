# Generated by Django 4.1.7 on 2023-05-11 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vk_api_app', '0013_rename_search_item_vkpost_analysed_item'),
        ('monitoring', '0039_rename_groupanalyzeditems_groupsearchitems_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SearchItem',
            new_name='AnalyzedItem',
        ),
        migrations.RenameModel(
            old_name='SearchItemKeywords',
            new_name='AnalyzedItemKeywords',
        ),
        migrations.RenameModel(
            old_name='SearchItemsSummaryStatistics',
            new_name='AnalyzedItemsSummaryStatistics',
        ),
        migrations.RenameModel(
            old_name='GroupSearchItems',
            new_name='GroupAnalyzedItems',
        ),
    ]
