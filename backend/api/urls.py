from apps.authentication.views import RegisterAPI, LoginAPI
from apps.posts.view import PostViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/v1/posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/auth/register/', RegisterAPI.as_view()),
    path('api/v1/auth/login/', LoginAPI.as_view()),
]