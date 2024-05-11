from django.contrib import admin
from .models import Exam, ExamAttempt, TestAttempt


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'creator', 'admin_created']


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'exam', 'student']

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['pk']