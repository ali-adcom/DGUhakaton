from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from datetime import datetime 
from tasks.models import Task
from tasks.serializers import TaskSerializer


@api_view(['GET']) 
def get_main_page(request): 
    user = request.user 
    today = datetime.today().date()
    daily_tasks = Task.objects.filter(family=user.family, created_datetime__date=today)
    tasks_serializer = TaskSerializer(daily_tasks, many=True)
    completed_tasks = Task.objects.filter(closed_by=user).count()
    user_score = { 'username': user.first_name + ' ' + user.last_name, 
                  'completed_tasks': completed_tasks,
                  }
    return Response({'daily_tasks': tasks_serializer.data, 'user_score': user_score }, status=status.HTTP_200_OK)