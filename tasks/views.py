from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(
    CreateModelMixin, 
    DestroyModelMixin, 
    UpdateModelMixin, 
    RetrieveModelMixin, 
    GenericViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    
    @action(detail=True, methods=['POST'], url_path='complete')
    def complete_task(self, request, *args, **kwargs):
        task = self.get_object()
        
        if request.user.family != task.family: 
            return Response({'error': 'Вы не можете закрывать задачи другой семьи'}, status=status.HTTP_403_FORBIDDEN) 
            
        task.is_completed = True
        task.closed_datetime = datetime.now() 
        task.closed_by = request.user 
        task.save()
        
        serializer = self.get_serializer(task) 
        
        return Response(serializer.data)
