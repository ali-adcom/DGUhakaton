from rest_framework import routers

from .views import TaskViewSet

tasks_router = routers.SimpleRouter()
tasks_router.register(r'', TaskViewSet, basename='tasks')