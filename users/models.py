from django.contrib.auth.models import AbstractUser
from django.db import models


class Family(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')
    avatar = models.ImageField(upload_to='family_avatars/', null=True, blank=True, verbose_name='Аватар')
    admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='admin_families', verbose_name='Администратор')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Семья'
        verbose_name_plural = 'Семьи'
        ordering = ['title']


class User(AbstractUser):
    KIND_CHOICES = [
        ('d', 'Папа'),
        ('m', 'Мама'),
        ('c', 'Ребенок'),
    ]

    kind = models.CharField(max_length=3, choices=KIND_CHOICES, null=True, verbose_name='Тип')
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='members', verbose_name='Семья')
    invite_code = models.CharField(max_length=64, null=True, blank=True, verbose_name='Код приглашения')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']
