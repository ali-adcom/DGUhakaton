from django.contrib import admin
from .models import Tag, Task, TaskImages

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'complexity', 'scope', 'family', 'is_completed', 'created_datetime', 'closed_datetime')
    list_filter = ('complexity', 'scope', 'family', 'is_completed')
    search_fields = ('title', 'desc', 'tags__title', 'family__name')
    autocomplete_fields = ('tags', 'family')

@admin.register(TaskImages)
class TaskImagesAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'image')
    search_fields = ('task__title', 'user__username')

