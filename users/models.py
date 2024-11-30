from django.db import models


class Families(models.Model):
    # Определите поля модели Family здесь
    title = models.CharField(max_length=128)  # Пример поля

    def __str__(self):
        return self.name

class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    KIND_CHOICES = [
        ('d', 'Папа'),
        ('m', 'Мама'),
        ('c', 'Ребенок'),
    ]
    kind = models.CharField(max_length=3, choices=KIND_CHOICES, null=True)
    family = models.ForeignKey(Families, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
