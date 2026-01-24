from rest_framework import serializers
from .model import Profile

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name']
        read_only_fields = fields