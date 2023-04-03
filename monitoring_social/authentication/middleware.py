from django.shortcuts import redirect
from django.urls import reverse


class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_urls = [
            reverse('sign_in_page'),
            reverse('sign_up_page'),
            reverse('home'),
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path not in self.allowed_urls:
                return redirect(reverse('sign_in_page'))
        response = self.get_response(request)
        return response
