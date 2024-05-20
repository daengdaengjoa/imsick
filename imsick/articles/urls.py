
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.HospitalAPIView.as_view(), name = "hospital"),
    path("detail/<int:article_id>/", views.HospitalDetailAPIView.as_view(), name = "detail"),
]