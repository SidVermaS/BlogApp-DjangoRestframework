from django.db import transaction
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer
from core.constants import ALLOWED_HTTP_METHODS
from core.pagination import DefaultLimitOffsetPagination


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author')
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ALLOWED_HTTP_METHODS

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return PostListSerializer
            case 'retrieve':
                return PostDetailSerializer
            case 'create':
                return PostCreateSerializer
            case 'update' | 'partial_update':
                return PostUpdateSerializer
            case _:
                return PostListSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        # self.perform_create(serializer)
        serializer.save()

        detail_serializer = PostDetailSerializer(serializer.instance, context={
            'request': request
        })

        return Response({ 'success': True, 'data': detail_serializer.data }, status = status.HTTP_201_CREATED)
    
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        detail_serializer=PostDetailSerializer(serializer.instance, context={'request':request})
        return Response({ 'success': True, 'data': detail_serializer.data }, status = status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # fallback (rare, but correct)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)