from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin):
    model = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()