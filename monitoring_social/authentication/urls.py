from django.urls import path, include
from authentication.views import *


urlpatterns = [
    path('auth/sign-in/', SignInPage.as_view(), name='sign_in_page'),
    path('auth/sign-up/', SignUpPage.as_view(), name='sign_up_page'),
    path('auth/logout/', logout_user, name='logout')
]
