from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class TaskPattern(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    COMPLEXITY_CHOICES = [
        (1, 'Легкая'),
        (2, 'Нормальная'),
        (3, 'Сложная'),
    ]
    complexity = models.IntegerField(choices=COMPLEXITY_CHOICES)
    recommend_time_in_min = models.SmallIntegerField()
    SCOPE_CHOICES = [
        ('in_family', 'Внутри семьи'),
        ('rating', 'Рейтинговая'),
    ]
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)

    def __str__(self):
        return self.title


class Task(models.Model):
    task_pattern = models.ForeignKey(TaskPattern, on_delete=models.CASCADE)
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    closed_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task {self.id} - {self.task_pattern.title}"


class TaskImage(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='task_images/')

    def __str__(self):
        return f"Image for {self.task}"
