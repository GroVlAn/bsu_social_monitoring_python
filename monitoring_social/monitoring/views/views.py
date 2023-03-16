from django.http import HttpResponse
from django.shortcuts import render, redirect

from monitoring.forms.OrganizationForm import OrganizationForm


def index(request):
    return render(request, 'monitoring/index.html')


def main(request):
    return render(request, 'monitoring/main/index.html')


def organization(request):
    print(request.method == 'POST')
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            try:
                form.save()
                return redirect('organization')
            except:
                form.add_error(None, 'Ошибка создания организации')
    else:
        form = OrganizationForm()
    context = {
        'title': 'Создание организации',
        'form': form
    }
    return render(request, 'monitoring/organization/create/index.html', context)
