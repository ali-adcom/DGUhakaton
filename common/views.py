from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status 
from datetime import datetime 
from tasks.models import Task
from tasks.serializers import TaskSerializer


@api_view(['GET']) 
def get_main_page(request): 
    user = request.user 

    data = dict()
    
    if user.is_authenticated:
        today = datetime.today().date()
        daily_rating_tasks = Task.objects.filter(family=user.family, created_datetime__date=today, scope='rating')
        tasks_serializer = TaskSerializer(daily_rating_tasks, many=True)

        data.update(
            {
                'username': f'{user.first_name} {user.first_name}', 
                'daily_tasks': tasks_serializer.data,
            }
        )

    return Response(data)
