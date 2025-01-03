"""django_conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common.views import get_main_page
from users.urls import users_router, families_router
from tasks.urls import tasks_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include(users_router.urls)),
    path('api/v1/families/', include(families_router.urls)),
    path('api/v1/tasks/', include(tasks_router.urls)),
    path('api/v1/get_main_page/', get_main_page, name='get_main_page'),
]
