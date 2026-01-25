from apps.authentication.views import RegisterAPIView, LoginAPIView
from apps.posts.views import PostViewSet
from apps.likes.views import LikesAPIView
from apps.comments.views import CommentViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/v1/posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/auth/register/', RegisterAPIView.as_view()),
    path('api/v1/auth/login/', LoginAPIView.as_view()),
    path('api/v1/posts/<uuid:post_id>/like/', LikesAPIView.as_view(), name='posts-like'),  
    path('api/v1/posts/<uuid:post_id>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='posts-comments'),
    path('api/v1/posts/<uuid:post_id>/comments/<uuid:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='posts-comments-id'),
]