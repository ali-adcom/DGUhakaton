from rest_framework import routers

from .views import UserViewSet, FamilyViewSet

users_router = routers.SimpleRouter()
users_router.register(r'', UserViewSet, basename='users')

families_router = routers.SimpleRouter()
families_router.register(r'', FamilyViewSet, basename='families')
