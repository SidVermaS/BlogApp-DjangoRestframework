from rest_framework import serializers
from django.db import IntegrityError
from apps.profiles.serializers import AuthorSerializer
from .mixins import PostValidationMixin
from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content',  'author', 'likes_count', 'comments_count', 'created_at']
        read_only_fields = fields

class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content',  'author', 'likes_count', 'comments_count', 'created_at']
        read_only_fields = fields

class PostCreateSerializer(PostValidationMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        try:
            return Post.objects.create(author = request.user, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError('title already exists')

    class Meta:
        model = Post
        fields = ['title', 'content', ]
        
class PostUpdateSerializer(PostValidationMixin, serializers.ModelSerializer):
    title = serializers.CharField(required = False)
    content = serializers.CharField(required = False)
    # image = serializers.ImageField(required = False)

    class Meta:
        model = Post
        fields = ['title', 'content',]