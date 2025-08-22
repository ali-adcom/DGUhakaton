from django.db.models import Sum, Q

from rest_framework.decorators import api_view 
from rest_framework.response import Response
from datetime import datetime 
from common.services import get_tasks_month_filter
from tasks.models import Task
from tasks.serializers import TaskSerializer
from users.models import Family
from users.serializers import FamilyRatingSerializer


@api_view(['GET']) 
def get_main_page(request): 
    user = request.user 

    data = dict()
    today = datetime.today().date()


    if user.is_authenticated:
        daily_rating_tasks = Task.objects.filter(family=user.family, created_datetime__date=today, scope='rating')
        tasks_serializer = TaskSerializer(daily_rating_tasks, many=True)

        data.update(
            {
                'username': f'{user.first_name} {user.first_name}', 
                'daily_tasks': tasks_serializer.data,
            }
        )

    tasks_month_filter = get_tasks_month_filter(month=today.month, year=today.year)
    rated_families = Family.objects.all().annotate(total_rating=Sum('tasks__complexity', filter=tasks_month_filter & Q(tasks__is_completed=True))).order_by('total_rating')
    family_serailizer = FamilyRatingSerializer(rated_families, many=True)
    
    data.update(
        {
            'rated_families': family_serailizer.data,
        }
    )

    return Response(data)
