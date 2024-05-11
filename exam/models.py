from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from math_app.models import *
from django.utils.timezone import now

from users.models import User


class Exam(models.Model):
    """
    Модель для организации данных о варианте экзамена ОГЭ по математике.

    **Поля:**

    - `time_create`: `DateTimeField` — время создания контрольной, добавляется автоматически при создании объекта.
    - `creator`: `ForeignKey` на модель `User` — пользователь, создавший контрольную. Может быть пустым или `null`.
    - `tests`: `ManyToManyField` на модель `Test` — тесты, включенные в контрольную.
    - `admin_created`: `BooleanField` — флаг, указывающий, создан ли вариант администратором. По умолчанию `False`.
    """
    time_create = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    tests = models.ManyToManyField(Test)
    admin_created = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        ordering = ('time_create',)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('exam', kwargs={'variant_id': self.pk})


class ExamAttempt(models.Model):
    """
    Модель для учета попыток прохождения экзамена учениками.

    **Поля:**

    - `student`: `ForeignKey` на модель `User` (связано с `related_name='exam_attempts'`) — ученик, проходящий экзамен.
    - `exam`: `ForeignKey` на модель `Exam` — вариант экзамена, который выполняется.
    - `score`: `IntegerField` — текущий набранный балл. Может быть `null` или пустым.
    - `max_score`: `IntegerField` — максимальный возможный балл. Может быть `null` или пустым.
    - `geometry_score`: `IntegerField` — балл за выполнение заданий по геометрии. Может быть `null` или пустым.
    - `mark`: `CharField` (максимальная длина 1) — итоговая оценка, если есть. Может быть `null` или пустым.
    - `time_spent`: `DurationField` — время, затраченное на выполнение варианта.
    - `completed_date`: `DateTimeField` — время завершения варианта, по умолчанию текущее время.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)
    geometry_score = models.IntegerField(null=True, blank=True)
    mark = models.CharField(max_length=1, null=True, blank=True)
    time_spent = models.DurationField()
    completed_date = models.DateTimeField(default=now)


class TestAttempt(models.Model):
    """
    Модель для хранения попыток прохождения тестов в рамках экзамена.

    **Поля:**

    - `student`: `ForeignKey` на модель `User` (связано с `related_name='test_attempts'`) — ученик, выполняющий тест.
    - `exam_attempt`: `ForeignKey` на модель `ExamAttempt` (связано с `related_name='question_attempts'`) — попытка выполнения экзамена, в рамках которой выполняется тест.
    - `test`: `ForeignKey` на модель `Test` — тест, который выполняется.
    - `answer`: `CharField` (максимальная длина 255) — текст ответа студента. Может быть `null` или пустым.
    - `completed_date`: `DateTimeField` — время завершения теста, добавляется автоматически при создании объекта.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='test_attempts')
    exam_attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True, blank=True)
    completed_date = models.DateTimeField(auto_now_add=True)
