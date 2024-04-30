from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    TEACHER = 'учитель'
    STUDENT = 'ученик'
    CHOICES = [
        (TEACHER, 'учитель'),
        (STUDENT, 'ученик')
    ]

    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    role = models.CharField(max_length=100, choices=CHOICES, default=STUDENT)
