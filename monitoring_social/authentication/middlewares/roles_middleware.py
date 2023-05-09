from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from rolepermissions.checkers import has_role

from monitoring.models_db.organization import Organization


class RequireRolesMiddleware:
    """
    Middleware for roles permissions
    :allowed_for_admin - field for allow admin` paths
    :not_allowed_for_employee - field for not allow employee` paths
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_for_admin = [
            reverse('admin:login'),
        ]
        self.not_allowed_for_employee = [
            reverse('edit_organization'),
            reverse('get_vk_api'),
        ]

    @staticmethod
    def check_needed_redirect_create_organization(*, path: str, user: User) -> bool:
        """If user is already create account, he needed to create new organization"""
        return not path == reverse('create_organization') and \
            not path == reverse('logout') and \
            not Organization.objects.filter(users=user) and \
            has_role(user, roles=['owner'])

    def __call__(self, request):
        """Checker allows paths"""
        user = request.user
        path = request.path
        if not user.is_authenticated:
            if path == 'admin' and not has_role(user=user, roles=('admin',)):
                return redirect(reverse('sign_in_page'))
        else:
            if path in self.allowed_for_admin and \
                    not has_role(user=user, roles=['admin', ]):
                return redirect(reverse('monitoring'))
            if path in self.not_allowed_for_employee and \
                    has_role(user=user, roles=['employee', ]):
                return redirect(reverse('monitoring'))
            if self.check_needed_redirect_create_organization(user=user, path=path):
                return redirect(reverse('create_organization'))
        response = self.get_response(request)
        return response
