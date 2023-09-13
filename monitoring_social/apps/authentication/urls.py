from django.urls import path, re_path

from apps.authentication.views import (
    SignInPage,
    SignUpPage,
    logout_user,
    InviteUserView
)

urlpatterns = [
    path('auth/sign-in/', SignInPage.as_view(), name='sign_in_page'),
    path('auth/sign-up/', SignUpPage.as_view(), name='sign_up_page'),
    path('auth/logout/', logout_user, name='logout'),
    path('settings/invite/', InviteUserView.as_view(), name='invite_user')
]
