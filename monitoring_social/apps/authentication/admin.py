from django.contrib import admin

from apps.authentication.models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invitation, InvitationAdmin)
