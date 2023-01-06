
from django.http import HttpResponse
from django.core import serializers

from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer

from rest_framework import permissions, viewsets, generics, mixins


class UsersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows todos to be viewed or edited.
    """
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated] # [permissions.AllowAny]

    def create(self, request):
        todo = Todo.objects.create(title=request.data.get('title', ''),
            description=request.data.get('description', ''),
            user=request.user,)
        serialized_obj = serializers.serialize('json', [todo,])
        return HttpResponse(serialized_obj, content_type='application/json')