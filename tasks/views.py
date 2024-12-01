from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin):
    model = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset
    
    
    @action(detail=True, methods=['POST'], url_path='complete', serializer_class=TaskSerializer)
    def complete_task(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user.family != task.family.admin: 
            return Response({'error': 'Ты не глава семьи'}, status=status.HTTP_403_FORBIDDEN) 
        task.is_completed = True
        task.closed_datetime = datetime.now() 
        task.closed_by = request.user 
        task.save()
        serializer = self.get_serializer(task) 
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)