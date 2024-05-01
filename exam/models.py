
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from math_app.models import *

from users.models import User


class Exam(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)
    admin_created = models.BooleanField(blank=True, null=True, default=False)


    class Meta:
        ordering = ('time_create',)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('exam', kwargs={'variant_id': self.pk})

class ExamAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()  # Может быть вычисляемым полем, если логика оценки сложная
    time_spent = models.DurationField()
    completed_date = models.DateTimeField(auto_now_add=True)

class TestAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    exam_attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)  # или любой другой формат, в зависимости от типа вопроса
    completed_date = models.DateTimeField(auto_now_add=True)
