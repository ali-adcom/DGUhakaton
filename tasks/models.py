from django.db import models

from users.models import Family, User


class Tag(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Task(models.Model):
    COMPLEXITY_CHOICES = [
        (10, 'Легкая'),
        (20, 'Нормальная'),
        (30, 'Сложная'),
    ]

    SCOPE_CHOICES = [
        ('in_family', 'Внутри семьи'),
        ('rating', 'Рейтинговая'),
    ]

    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    tags = models.ManyToManyField(Tag, related_name='tasks', verbose_name='Теги')
    complexity = models.IntegerField(choices=COMPLEXITY_CHOICES, verbose_name='Сложность задачи')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, verbose_name='Область видимости')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name='Семья')
    is_completed = models.BooleanField(default=False, verbose_name='Завершено?')
    recommend_time_in_min = models.SmallIntegerField(verbose_name='Рекомендуемое время в минутах')
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    closed_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    closed_by = models.ForeignKey(User, null=True, blank=True, verbose_name='Кем завершена')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskReportFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file_url = models.CharField(max_length=256, verbose_name='URL к файлу')

    def __str__(self):
        return f"Image for {self.task} by {self.user.username}"
    
    class Meta:
        verbose_name = 'Файл отчета по задаче'
        verbose_name_plural = 'Файлы отчетов по задачам'
