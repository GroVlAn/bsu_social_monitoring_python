from monitoring.models_db.AnalyzedItems import AnalyzedItemsSummaryStatistics


def create_organization(request, form) -> None:
    form.save()
    form.save(user=request.user)


def create_analysed_item(form) -> None:
    analyzed_item = form.save(commit=False)  # сохраняем объект AnalyzedItem без сохранения в БД
    analyzed_item.save()  # сохраняем объект AnalyzedItem в БД
    # создаем объект AnalysedItemsSummaryStatistics с отношением "один к одному" к сохраненному объекту AnalyzedItem
    summary_statistics = AnalyzedItemsSummaryStatistics.objects.create(owner=analyzed_item)
