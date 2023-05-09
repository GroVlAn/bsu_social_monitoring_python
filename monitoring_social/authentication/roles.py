from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    """Admin role, only this role have access to admin page"""
    available_permissions = {
        'access_admin_page': True,
    }


class Owner(AbstractUserRole):
    """Owner role, this is creator main account"""
    available_permissions = {
        'create_team': True,
        'edit_monitoring_settings': True,
        'edit_team_settings': True,
        'edit_vk_settings': True,
        'delete_items': True
    }


class Employee(AbstractUserRole):
    available_permissions = {
        'create_team': False,
        'edit_monitoring_settings': True,
        'edit_team_settings': True,
        'edit_vk_settings': True,
        'delete_items': False
    }
