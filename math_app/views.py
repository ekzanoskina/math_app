from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *

# Create your views here.

class Home(ListView):
    model = Category
    template_name = 'math_app/index.html'
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}

class ShowSubcategory(ListView):
    model = Exercise
    template_name = 'math_app/exercises_list.html'
    context_object_name = 'exercises'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вид - ' + str(context['exercises'][0].subcategory.title).lower()
        return context

    def get_queryset(self):
        return Exercise.objects.filter(subcategory__slug=self.kwargs['subcat_slug'])

class ShowTest(DetailView):
    model = Test
    template_name = 'math_app/test_detail.html'
    context_object_name = 'test'
    pk_url_kwarg = 'test_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тест id №' + str(context['test'].pk)
        return context

