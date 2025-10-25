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

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class TaskRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= TaskSerializer
    queryset=TaskModel.objects.all()
    lookup_field='pk'

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class AccountCreate(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=AccountSerializers
    queryset=User.objects.all()

