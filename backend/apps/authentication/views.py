from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.serializers import RegisterSerializer, LoginSerializer

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
    
class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data, context = { "request": request })
        serializer.is_valid(raise_exception = True)

        return Response({ "message": "Login successful", "data": serializer.validated_data}, status = status.HTTP_200_OK)