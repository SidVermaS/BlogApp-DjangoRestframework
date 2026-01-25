from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from core.constants import ALLOWED_HTTP_METHODS
from core.pagination import DefaultLimitOffsetPagination
from .models import Comment
from .serializers import CommentCreateSerializer, CommentUpdateSerializer, CommentDetailedSerializer, CommentListSerializer

class CommentViewSet(ModelViewSet):

    authentication_classes=[JWTAuthentication]
    filter_backends = [OrderingFilter]
    http_method_names = ALLOWED_HTTP_METHODS
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.select_related('author', 'post')

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CommentListSerializer
            case 'create':
                return CommentCreateSerializer
            case 'partial_update' | 'update':
                return CommentUpdateSerializer
            case _:
                return CommentDetailedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset
    
    def get_object(self):
        post_id = self.kwargs['post_id']
        id = self.kwargs['pk']
        return get_object_or_404(self.get_queryset(), post_id=post_id, id = id)

    def list(self, request, *args, **kwargs):
        queryset =self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, post_id, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, context = {'request': request, 'post_id': post_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detailed_serializer = CommentDetailedSerializer(serializer.instance)
        return Response({'success': True, 'data':detailed_serializer.data}, status = status.HTTP_201_CREATED)
    
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = CommentDetailedSerializer(serializer.instance)
        return Response({ 'success': True, 'data': detail_serializer.data }, status = status.HTTP_200_OK)
    
    # def destroy(self, request, *args, **kwargs):
