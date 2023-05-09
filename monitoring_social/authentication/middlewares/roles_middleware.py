from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.permissions import available_perm_status
from rolepermissions.roles import get_user_roles

from monitoring.models_db.team import Team


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
            reverse('edit_team'),
            reverse('get_vk_api'),
        ]

    @staticmethod
    def check_needed_redirect_create_team(*, path: str, user: User) -> bool:
        """If user is already create account, he needed to create new team"""
        return not path == reverse('create_team') and \
            not path == reverse('logout') and \
            not Team.objects.filter(users=user) and \
            has_permission(user, permission_name='create_team')

    def __call__(self, request):
        """Checker allows paths"""
        user = request.user
        path = request.path
        if not user.is_authenticated:
            if path == 'admin' and not has_role(user=user, roles=('admin',)):
                return redirect(reverse('sign_in_page'))
        else:
            if path in self.allowed_for_admin and \
                    not has_permission(user=user, permission_name='access_admin_page'):
                return redirect(reverse('monitoring'))
            print(available_perm_status(user=user))
            if path in self.not_allowed_for_employee and \
                    not has_permission(user=user, permission_name='edit_team_settings'):
                return redirect(reverse('monitoring'))
            if self.check_needed_redirect_create_team(user=user, path=path):
                return redirect(reverse('create_team'))
        response = self.get_response(request)
        return response
