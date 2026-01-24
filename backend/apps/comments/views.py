from rest_framework.viewsets import ModelViewSet
from .serializers import CommentCreateSerializer, CommentUpdateSerializer

class CommentViewSet(ModelViewSet):
    def get_serializer_class(self):
        match self.action:
            case 'create':
                return CommentCreateSerializer
            case 'partial_update' | 'update':
                return CommentUpdateSerializer

    def create(self, request, post_id):
        serializer = self.get_serializer(data = request.data, context = {'request': request, 'post_id': post_id})
        serializer.save()
        
        