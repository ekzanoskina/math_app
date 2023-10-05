from django.contrib.messages.storage import session
from django.forms import formset_factory
from django.db.models import Q
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from math_app.models import *
from .forms import *
from .models import *
import random
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView


def show_progress(request, variant_id):
    if variant_id:
        variant = Variant.objects.get(pk=variant_id)
        tests_part1 = Test.objects.filter(Q(exercise__in=variant.exercise.all()) & Q(exercise__subcategory__category__id__lt=20))
        tests_part2 = Test.objects.filter(Q(exercise__in=variant.exercise.all()) & Q(exercise__subcategory__category__id__gt=19))

    else:
        tests_part1 = Test.objects.filter(Q(exercise__id__in=request.session['exercises_list']) & Q(exercise__subcategory__category__id__lt=20))
        tests_part2 = Test.objects.filter(Q(exercise__id__in=request.session['exercises_list']) & Q(exercise__subcategory__category__id__gt=19))
    tests = tests_part1 | tests_part2
    answers = request.session.get('dict_answers')
    correct_answers = request.session.get('dict_correct_answers')
    dict_part2_points = request.session.get('dict_part2_points')
    time = request.session.get('time')
    max_result = tests_part1.count() + (tests_part2.count() * 2)
    result = len(correct_answers)
    geometry_result = len([val for key, val in correct_answers.items() if Test.objects.get(id=key).get_category_id() in [15, 16, 17, 18, 19]])
    if len(dict_part2_points) > 0:
        result += sum([int(point) for point in dict_part2_points.values() if point != None])
        geometry_result += sum([int(val) for key, val in dict_part2_points.items() if Test.objects.get(id=key).get_category_id() in [23, 24, 25] and val != None])
    mark = '2'
    if geometry_result >= 2:
        if 8 <= result < 15:
            mark = '3'
        elif 15 <= result < 22:
            mark = '4'
        elif result >= 22:
            mark = '5'
    return render(request, 'exam/progress.html', {'variant_id': variant_id, 'tests': tests, 'tests_part1': tests_part1, 'tests_part2': tests_part2, 'correct_answers': correct_answers, 'answers': answers, 'time': time, 'max_result': max_result, 'result': result, 'geometry_result': geometry_result, 'mark': mark})

def take_exam2(request, variant_id):
    if variant_id:
        variant = Variant.objects.get(pk=variant_id)
        tests = Test.objects.filter(Q(exercise__in=variant.exercise.all()) & Q(exercise__subcategory__category__id__gt=19)).order_by('exercise__subcategory__category__id')
    else:
        tests = Test.objects.filter(Q(exercise__in=request.session['exercises_list']) & Q(exercise__subcategory__category__id__gt=19)).order_by('exercise__subcategory__category__id')
    num_tests = tests.count()
    QuestionFormSet = formset_factory(form=QuestionForm, formset=BaseExamFormSet, extra=num_tests)
    dict_part2_points = {}
    dict_answers = request.session.get('dict_answers')
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, form_kwargs={'tests': list(tests)})
        if formset.is_valid():
            for form in formset:
                test = form.test
                answer = form.cleaned_data.get('answers')
                dict_part2_points[test.id] = answer
                dict_answers[test.id] = answer
            request.session['dict_part2_points'] = dict_part2_points

            return redirect('progress', variant_id = variant_id)
    else:
        formset = QuestionFormSet(form_kwargs={'tests': list(tests)})
        return render(request, 'exam/exam2.html', {'tests': tests, 'formset': formset})

def take_exam(request, variant_id):
    if variant_id:
        variant = Variant.objects.get(pk=variant_id)
        tests = Test.objects.filter(exercise__in=variant.exercise.all()).order_by('exercise__subcategory__category__id')
    else:
        tests = Test.objects.filter(exercise__in=request.session.get('exercises_list')).order_by('exercise__subcategory__category__id')
    num_tests = tests.count()
    ExamFormSet = formset_factory(form=EssayForm, formset=BaseExamFormSet, extra=num_tests)
    if request.method == 'POST':
        request.session['time'] = request.POST.get('time')
        formset = ExamFormSet(request.POST, form_kwargs={'tests': list(tests)})
        dict_correct_answers = {}
        dict_answers = {}
        if formset.is_valid():
            for form in formset:
                test = form.test
                answer = form.cleaned_data.get('answers')
                dict_answers[test.id] = answer
                if answer in test.get_answers():
                    dict_correct_answers[test.id] = answer
                request.session['dict_correct_answers'] = dict_correct_answers
                request.session['dict_answers'] = dict_answers
            if tests.filter(exercise__subcategory__category__id__gt=19).count() > 0:
                return redirect('exam2', variant_id=variant_id)
            else:
                request.session['dict_part2_points'] = {}
                return redirect('progress', variant_id=variant_id)
    else:
        formset = ExamFormSet(form_kwargs={'tests': list(tests)})
    return render(request, 'exam/exam.html', {'formset': formset})


#
def exam_filter(request):
    categories = Category.objects.all()
    num_cat = categories.count()
    lst = []
    FilterFormSet = formset_factory(form=FilterForm, formset=BaseFilterFormSet, extra=num_cat, max_num=num_cat, min_num=1, validate_min=True)
    if request.method == 'POST':
        formset = FilterFormSet(request.POST, form_kwargs={'categories': categories})

        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    cat_quantity = form.cleaned_data.get('cat_quantity')
                    subcategory = form.cleaned_data['subcategory']
                    if cat_quantity:
                        exercises = Exercise.objects.filter(subcategory__in=subcategory).order_by('?')[:cat_quantity]
                        for ex in exercises:
                            lst.append(ex.id)
            request.session['exercises_list'] = lst
            return redirect('exam', variant_id=0)

    else:
        formset = FilterFormSet(form_kwargs={'categories': list(categories), })
    return render(request, 'exam/exam_filter.html', {'formset': formset})

class ShowVariant(ListView):
    model = Variant
    template_name = 'exam/variants.html'
    context_object_name = 'variants'



