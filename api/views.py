from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import TaskSerializer,AccountSerializers
from task.models import TaskModel
from django.contrib.auth.models import User
from .paginations import TasksPagination
from .filters import TaskFilter

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class= TaskSerializer
    queryset=TaskModel.objects.all()
    pagination_class=TasksPagination
    filterset_class=TaskFilter
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= TaskSerializer
    queryset=TaskModel.objects.all()
    lookup_field='pk'
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user).order_by('-created_at')

class AccountCreate(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=AccountSerializers
    queryset=User.objects.all()

