# urls.py
from django.urls import path
from .views import UserCreateView, VerifyEmailView

urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user_register'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
