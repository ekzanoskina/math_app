
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from math_app.models import *


class Variant(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    exercise = models.ManyToManyField(Exercise)

    class Meta:
        ordering = ('time_update',)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('exam', kwargs={'variant_id': self.pk})

# class ExamAttempt(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     score = models.FloatField()  # Может быть вычисляемым полем, если логика оценки сложная
#     time_spent = models.DurationField()
#     completed_date = models.DateTimeField()
#
# class QuestionAttempt(models.Model):
#     exam_attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='question_attempts')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.CharField(max_length=255)  # или любой другой формат, в зависимости от типа вопроса
#     correct = models.BooleanField()
#     time_spent = models.DurationField()
