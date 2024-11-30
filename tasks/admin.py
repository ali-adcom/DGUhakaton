from django.contrib import admin

from .models import Tag, Task, TaskReportFile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'complexity', 'scope', 'family', 'is_completed', 'created_datetime', 'closed_datetime', 'closed_by')
    list_filter = ('complexity', 'scope', 'family', 'is_completed')
    search_fields = ('title', 'tags__title', 'family__name')
    autocomplete_fields = ('tags', 'family')
    readonly_fields = ('closed_datetime', 'created_datetime')


@admin.register(TaskReportFile)
class TaskReportFileAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'image')
    search_fields = ('task__title', 'user__username')

