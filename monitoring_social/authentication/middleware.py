from django.shortcuts import redirect
from django.urls import reverse
from rolepermissions.checkers import has_role


class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_urls = [
            reverse('sign_in_page'),
            reverse('sign_up_page'),
            reverse('home'),
        ]
        self.allowed_for_admin = [
            reverse('admin:login'),
        ]
        self.not_allowed_for_employee = [
            reverse('edit_team'),
            reverse('get_vk_api'),
        ]

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
            if request.path == 'admin' and not has_role(user=user, roles=('admin',)):
                return redirect(reverse('sign_in_page'))
            if request.path not in self.allowed_urls:
                return redirect(reverse('sign_in_page'))
        else:
            if request.path in self.allowed_for_admin and not has_role(user=user, roles=('admin',)):
                return redirect(reverse('monitoring'))
        response = self.get_response(request)
        return response
