from rest_framework.serializers import ModelSerializer, CharField
from django.shortcuts import get_object_or_404
from apps.posts.models import Post
from .models import Comment
from .mixins import CommentValidationMixin
from apps.profiles.serializers import AuthorSerializer


class CommentListSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id','text','created_at','author']
        read_only_fields = fields


class CommentCreateSerializer(CommentValidationMixin, ModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        post_id = self.context['post_id']

        post = get_object_or_404(Post, post_id)
        
        return Comment.objects.create(post = post, author = request.user, **validated_data)


    class Meta:
        model = Comment
        fields = ['text']


class CommentUpdateSerializer(CommentValidationMixin, ModelSerializer):
    text = CharField(min=1, max=100, required = True)

    class Meta:
        model = Comment
        fields = ['text']


class CommentDetailedSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']
        read_only_fields = fields