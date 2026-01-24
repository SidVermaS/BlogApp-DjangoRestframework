from apps.authentication.views import RegisterAPI, LoginAPI
from backend.apps.posts.views import PostViewSet
from apps.likes.views import LikesAPIView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/v1/posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/auth/register/', RegisterAPI.as_view()),
    path('api/v1/auth/login/', LoginAPI.as_view()),
    path('api/v1/posts/<uuid:post_id>/likes', LikesAPIView.as_view(), name='posts-likes')
]