from django.contrib import admin

from users.models import User, Family


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'family')
    list_filter = ('role', 'family')
    search_fields = ('username', 'first_name', 'last_name', 'family__title')


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin')
    search_fields = ('title',)
