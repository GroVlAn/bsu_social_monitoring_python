from django.shortcuts import render


def signIn(request):
    return render(request, 'authentication/sign-in/index.html')


def signUp(request):
    return render(request, 'authentication/sign-up/index.html')
