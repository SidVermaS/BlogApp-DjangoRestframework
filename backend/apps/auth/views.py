from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.apps.auth.serializers import RegisterSerializer

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)