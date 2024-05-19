from django.contrib import admin
import nested_admin
from .models import *


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'title']
    prepopulated_fields = {'slug': ('title',)}
class SubcategoryInline(admin.StackedInline):
    model = Subcategory
    prepopulated_fields = {'slug': ('title',)}
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SubcategoryInline,]
    list_display = ['number', 'title']




class CategoryInline(admin.StackedInline):
    model = Category
    extra = 1

class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 1
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines=[AnswerInline, ]
    list_filter = ["exercise__subcategory__category__id"]
class TestInline(nested_admin.NestedStackedInline):
    model = Test
    inlines = [AnswerInline,]
    extra = 1

@admin.register(Exercise)
class ExerciseAdmin(nested_admin.NestedModelAdmin):
    list_display = ['id', 'subcategory']
    list_filter = ['id']
    search_fields = ['id', 'content']
    inlines = [TestInline,]




