from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from apps.profiles.models import Profile

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True, min_length = 8, max_length = 32)
    password_confirm = serializers.CharField(write_only=True, min_length = 8, max_length = 32)

    class Meta:
        model = Profile
        fields = ['email', 'name', 'password', 'password_confirm']

    def create(self, validated_data):
        validated_data.pop('password_confirm')           
       
        profile = Profile.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return profile
        
    def validate_email(self, value):
        if Profile.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()
    
    def validate(self, attrs):       
        if len(attrs['name'].strip()) < 2:
            raise serializers.ValidationError('Name must be at least 2 characters.')
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Password fields must match.')
        return attrs

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length = 8, max_length = 32, write_only = True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        profile = authenticate(request = self.context.get('request'), username = email, password = password)

        if not profile:
            raise serializers.ValidationError('Invalid email or password')
        if profile.status != Profile.Status.ACTIVE:
            raise serializers.ValidationError("Account is blocked")
        
        access_token = AccessToken.for_user(profile)

        return {
            'access_token': str(access_token)
        }
        