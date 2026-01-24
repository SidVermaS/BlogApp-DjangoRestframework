from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.posts.models import Post
from .models import Like

class LikesAPIView(APIView):
    http_method_names = ['post', 'delete']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        _, created = Like.objects.get_or_create(post=post, profile=request.user)

        if created:
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') + 1)
            return Response({'success': True, 'message': 'Successfully liked'}, status=status.HTTP_201_CREATED)
        
        return Response({'success': True, 'message': 'Already liked'}, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        deleted, _ = Like.objects.filter(post=post, profile=request.user).delete()

        if deleted:
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') - 1)
            return Response({'success': True, 'message': 'Successfully unliked'}, status=status.HTTP_200_OK)
        
        return Response({'success': True, 'message': "Like didn't exist"}, status=status.HTTP_200_OK)
