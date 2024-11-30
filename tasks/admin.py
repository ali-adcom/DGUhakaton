from django.contrib import admin
from .models import Tag, TaskPattern, Task, TaskImage

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(TaskPattern)
class TaskPatternAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'complexity', 'recommend_time_in_min', 'scope')
    list_filter = ('complexity', 'scope')
    search_fields = ('title', 'tags__name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_pattern', 'family', 'is_completed', 'created_datetime', 'closed_datetime')
    list_filter = ('is_completed', 'created_datetime', 'closed_datetime')
    search_fields = ('task_pattern__title', 'family__name')

@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'image')
    list_filter = ('user', 'task')
    search_fields = ('user__first_name', 'user__last_name', 'task__task_pattern__title')
