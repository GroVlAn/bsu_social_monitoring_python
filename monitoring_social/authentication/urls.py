from django.urls import path
from authentication.views import signIn, signUp

urlpatterns = [
    path('auth/sign-in/', signIn),
    path('auth/sign-up/', signUp)
]
