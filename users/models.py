from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models

from users.validators import validate_age


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)



class Family(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')
    avatar = models.CharField(max_length=256, null=True, blank=True, verbose_name='Аватар')
    admin = models.OneToOneField(
        'User', on_delete=models.CASCADE, related_name='admin_family', verbose_name='Администратор'
    )
    rating = models.SmallIntegerField(default=0, verbose_name='Количество баллов')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Семья'
        verbose_name_plural = 'Семьи'


class User(AbstractBaseUser):
    KIND_CHOICES = [
        ('d', 'Папа'),
        ('m', 'Мама'),
        ('c', 'Ребенок'),
    ]

    GENDER_CHOICES = [
        ('m', 'Мужской'),
        ('f', 'Женский'),
    ]

    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(unique=True, max_length=256, verbose_name='E-mail')
    role = models.CharField(max_length=3, choices=KIND_CHOICES, null=True, verbose_name='Роль')
    family = models.ForeignKey(
        Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='members', verbose_name='Семья'
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='Пол')
    age = models.SmallIntegerField(verbose_name='Возраст', validators=[validate_age])
    is_staff = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'gender', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None): 
        return True 
    def has_module_perms(self, app_label): 
        return True
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FamilyInviteCode(models.Model):
    code = models.CharField(max_length=16, unique=True, verbose_name='Код')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name='Семья')