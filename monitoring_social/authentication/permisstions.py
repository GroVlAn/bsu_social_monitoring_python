from django.contrib.auth.models import User
from django.urls import reverse
from rolepermissions.checkers import has_role
from rolepermissions.permissions import register_object_checker


allowed_for_admin = {
    reverse('admin:login')
}


def access_admin(path: str, user: User):
    """Access to admin page only for admin"""
    if path in allowed_for_admin and has_role(user=user, roles=('admin',)):
        return True
    return False
