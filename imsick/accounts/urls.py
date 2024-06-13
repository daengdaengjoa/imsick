from django.urls import path
from .views import UserAPIView, LogoutView, PasswordUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("", UserAPIView.as_view(), name="user_list"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # 새로고침 엔드포인트 추가
    path("<str:username>/", UserAPIView.as_view(), name="profile_update"),
    path("<str:username>/password/",PasswordUpdateAPIView.as_view(), name="password_update"),
    ]