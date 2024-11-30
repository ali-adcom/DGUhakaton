from django.contrib import admin
from .models import Users, Families

@admin.register(Families)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'kind', 'family')
    list_filter = ('kind', 'family')
    search_fields = ('first_name', 'last_name', 'family__name')
