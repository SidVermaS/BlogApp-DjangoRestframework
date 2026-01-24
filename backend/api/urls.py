from backend.apps.auth import RegisterAPI, LoginAPI
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('api/v1/auth/register/', RegisterAPI.as_view()),
    path('api/v1/auth/login/', LoginAPI.as_view()),
]