from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Comment

class CommentValidationMixin:
    def validate_text(self, value):
        value = value.strip()
        if len(value) < 1:
            raise ValidationError('Comment cannot be empty.')
        if len(value) >100:
            raise ValidationError('Comment cannot exceed 100 characters.')
        return value