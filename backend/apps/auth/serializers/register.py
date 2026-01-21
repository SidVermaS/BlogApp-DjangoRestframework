from rest_framework import serializers
from django.db import IntegrityError, transaction
from backend.apps.profiles.model import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8, max_length = 32)
    password_confirm = serializers.CharField(write_only=True, min_length = 8, max_length = 32)

    class Meta:
        model = Profile
        fields = ['email', 'name', 'password', 'password_confirm']

    def create(self, validated_data):
        try:
            validated_data.pop('password_confirm')
            
            with transaction.atomic():
                profile = Profile.objects.create_user(
                    email=validated_data['email'],
                    password=validated_data['password'],
                    name=validated_data['name']
                )
                return profile
        except IntegrityError:
            raise serializers.ValidationError({
                "email":"Email already exists"
            })

    def validate(self, attrs):       
        if len(attrs['name'].strip()) < 2:
            raise serializers.ValidationError({
                'name': 'Name must be at least 2 characters.'
            })
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Password fields must match.'
            })
        return attrs