from rest_framework import serializers
from .models import Post
class PostValidationMixin:
    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError('title must be at least 3 characters long.')
        if len(value) > 100:
            raise serializers.ValidationError('title cannot exceed 100 characters.')
        queryset = Post.objects.filter(title__iexact = value)
        if self.instance:
            queryset = queryset.exclude(id = self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError('title already exists')
        return value
    
    def validate_content(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError('content must be at least 3 characters long.')
        return value