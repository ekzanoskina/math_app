from django.views.generic import ListView, DetailView
from .models import *

class Home(ListView):
    """Представление домашней страницы, отображает список категорий."""
    model = Category
    template_name = 'math_app/index.html'
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    def get_queryset(self):
        return Category.objects.all().prefetch_related('subcategory_set')

class ShowSubcategory(ListView):
    """Представление страницы подкатегорий, отображает упражнения выбранной подкатегории."""
    model = Exercise
    template_name = 'math_app/exercises_list.html'
    context_object_name = 'exercises'
    allow_empty = True  # Изменён на True для разрешения пустого queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     #     """Добавляет в контекст заголовок страницы с названием подкатегории."""
    #     #     context = super().get_context_data(**kwargs)
    #     #     context['title'] = 'Вид - ' + str(context['exercises'][0].subcategory.title).lower()
    #     #     return context
    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет в контекст заголовок страницы и сообщение о скором добавлении материалов, если список упражнений пуст."""
        context = super().get_context_data(**kwargs)
        if not context['exercises']:
            context['message'] = "Материал скоро будет добавлен."
            context['title'] = "Подкатегория"
        else:
            context['title'] = f"Вид - {context['exercises'][0].subcategory.title.lower()}"
        return context

    def get_queryset(self):
        return Exercise.objects.filter(subcategory__slug=self.kwargs['subcat_slug'])

class ShowTest(DetailView):
    """Представление детальной информации о тесте."""
    model = Test
    template_name = 'math_app/test_detail.html'
    context_object_name = 'test'
    pk_url_kwarg = 'test_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет в контекст заголовок страницы с номером теста."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тест id №' + str(context['test'].pk)
        return context

