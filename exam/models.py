
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
