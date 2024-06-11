# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView



urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # 기본 주소로 접속 시 인덱스 페이지
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),  # /signup/ 경로로 회원가입 페이지
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'), 
    path('makearticle/', TemplateView.as_view(template_name='makearticle.html'), name='makearticle'), 
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/articles/', include('articles.urls')),
]
