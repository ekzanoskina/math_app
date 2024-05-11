from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    """Категория заданий.

    Атрибуты:
        id (Integer): Уникальный идентификатор категории.
        number (CharField): Номер категории.
        title (CharField): Название категории.
        slug (SlugField): URL слаг категории.

    Метаинформация:
        ordering: Упорядочивание по идентификатору.
    """
    id = models.IntegerField(primary_key=True, unique=True)
    number = models.CharField(max_length=200, verbose_name='Номер')
    title = models.CharField(max_length=200, db_index=True, verbose_name='Тип')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    """Подкатегория заданий.

       Атрибуты:
           category (ForeignKey): Связь с категорией.
           title (CharField): Название подкатегории.
           slug (SlugField): URL слаг подкатегории.

       Метаинформация:
           ordering: Упорядочивание по категории.
       """
    category = models.ForeignKey(Category, verbose_name='Тип', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='Вид', db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('category',)

    def __str__(self):
        return f'{self.category.number} {self.title}'

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'subcat_slug': self.slug})

class Exercise(models.Model):
    """Упражнение. Введено специально над тестом, так как первые 5 номеров объединяет одна картинка и они не могут быть разделены в экзаменах.

    Атрибуты:
        subcategory (ForeignKey): Связь с подкатегорией.
        description (RichTextUploadingField): Описание упражнения.
        picture (ImageField): Изображение, связанное с упражнением.
        time_create (DateTimeField): Время создания упражнения.
        time_update (DateTimeField): Время последнего обновления упражнения.
        source (TextField): Источник информации упражнения.
    """
    subcategory = models.ForeignKey(Subcategory, related_name='subcategory', on_delete=models.CASCADE,
                                    verbose_name='Вид')
    description = RichTextUploadingField(blank=True, null=True)
    picture = models.ImageField(blank=True, upload_to="pictures/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    source = models.TextField(blank=True, verbose_name='Источник')
    def __str__(self):
        return f"{self.subcategory.title} {self.pk}"

class Test(models.Model):
    """Тест, связанный с упражнением. У первых 5 номеров связь упражнение -> тест - один ко многим, у остальных - один к одному.

    Атрибуты:
        exercise (ForeignKey): Связь с упражнением.
        problem_text (RichTextUploadingField): Текст задачи.
        time_create (DateTimeField): Время создания теста.
        time_update (DateTimeField): Время последнего обновления теста.
        solution (RichTextUploadingField): Решение задачи.
        criteria (RichTextUploadingField): Критерии оценивания.
        part2 (BooleanField): Отметка о том, что задача принадлежит к части 2.

    Метаинформация:
        ordering: Упорядочивание по идентификатору категории упражнения.
    """
    # category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name='Подвид')
    problem_text = RichTextUploadingField(blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    solution = RichTextUploadingField(blank=True, null=True, verbose_name='Решение')
    criteria = RichTextUploadingField(blank=True, null=True, verbose_name='Критерии')
    part2 = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('exercise__subcategory__category__id',)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('test', kwargs={'test_id': self.pk})

    def get_answers(self):
        ans_ls = []
        for ans in self.answer_set.all():
            ans_ls.append(str(ans))
        return ans_ls

    def get_category_id(self):
        return self.exercise.subcategory.category.id

    def get_category_number(self):
        return self.exercise.subcategory.category.number

class Answer(models.Model):
    exercise = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Задание')
    answer = models.CharField(verbose_name='Ответ', max_length=200, db_index=True, null=True, blank=True)
    def __str__(self):
        return self.answer