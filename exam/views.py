from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, BooleanField
from django.db.models import Q, Value, Count
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from math_app.models import *
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView
from django.core.cache import cache
from django.db.models import Case, When, IntegerField


def check_geometry():
    tests_geometry = cache.get('tests_geometry')
    if tests_geometry is None:
        # Using values_list with flat=True to get a list of ids directly
        tests_geometry = list(
            Test.objects.filter(exercise__subcategory__category__id__in=[15, 16, 17, 18, 19, 23, 24, 25]).values_list(
                'id', flat=True))
        cache.set('tests_geometry', tests_geometry)
    return tests_geometry


def get_tests(request, variant_id=None):
    variant = Exam.objects.prefetch_related('tests').get(pk=variant_id) if variant_id else None
    # exercise_in = variant.tests.all() if variant else request.session['tests_list']
    tests_qs = variant.tests.all() if variant else Test.objects.filter(id__in=request.session['tests_list']).select_related('exercise__subcategory__category')
    # print(variant.tests.all())
    # tests_qs = Test.objects.filter(id__in=exercise_in).select_related('exercise__subcategory__category')
    tests_qs = tests_qs.annotate(
        part_2=Case(
            When(exercise__subcategory__category__id__lt=20, then=False),
            When(exercise__subcategory__category__id__gt=19, then=True),
            default=False,
        )
    )
    tests = tuple(tests_qs.filter(part_2=value) for value in (False, True))

    return tests


def calculate_results(tests_part1_count, tests_part2_count, correct_answers, dict_part2_points):
    max_result = tests_part1_count + (tests_part2_count * 2)
    result = len(correct_answers)
    tests_geometry = check_geometry()
    geometry_result = sum([1 for key, val in correct_answers.items() if int(key) in tests_geometry])
    if dict_part2_points:
        result += sum([int(point) for point in dict_part2_points.values() if point is not None])
        geometry_result += sum(
            [int(val) for key, val in dict_part2_points.items() if int(key) in tests_geometry and val is not None])
    return max_result, result, geometry_result


def calculate_mark(geometry_result, result):
    mark = '2'
    if geometry_result >= 2:
        if 8 <= result < 15:
            mark = '3'
        elif 15 <= result < 22:
            mark = '4'
        elif result >= 22:
            mark = '5'
    return mark


def show_progress(request, variant_id=None):
    tests_part1, tests_part2 = get_tests(request, variant_id)
    tests = tests_part1.prefetch_related('answer_set') | tests_part2
    session = request.session
    tests_part1_count, tests_part2_count = session.get('tests_count')
    answers = session.get('dict_answers')
    correct_answers = session.get('dict_correct_answers')
    dict_part2_points = session.get('dict_part2_points')
    time = session.get('time')
    hours, minutes, seconds = map(int, time.split(':'))
    td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    max_result, result, geometry_result = calculate_results(tests_part1_count, tests_part2_count, correct_answers,
                                                            dict_part2_points)
    mark = calculate_mark(geometry_result, result)
    if not request.user.is_anonymous:
        if variant_id is None:
            exam = Exam.objects.create(creator=request.user)
            test_ids = [test.id for test in tests]
            exam.tests.add(*test_ids)
            exam.save()
        else:
            exam = Exam.objects.get(pk=variant_id)
        exam_attempt = ExamAttempt.objects.create(student=request.user, exam=exam, time_spent=td, max_score=max_result,
                                                      score=result, geometry_score=geometry_result, mark=mark)
        exam_attempt.save()
        for test_id, answer in answers.items():
            test = Test.objects.get(pk=test_id)
            test_attempt = TestAttempt.objects.create(student=request.user, exam_attempt=exam_attempt, test=test,
                                                          answer=answer)
            test_attempt.save()


    return render(request, 'exam/progress.html',
                  {'variant_id': variant_id, 'tests': tests, 'tests_part1': tests_part1, 'tests_part2': tests_part2,
                   'tests_part1_count': tests_part1_count, 'tests_part2_count': tests_part2_count,
                   'correct_answers': correct_answers, 'answers': answers, 'time': time, 'max_result': max_result,
                   'result': result, 'geometry_result': geometry_result, 'mark': mark})


def handle_exam(request, tests, num_tests, form_class, template_name, variant_id=None, tests_part2=None,
                category_group=0):
    dict_correct_answers = {}
    dict_part2_points = {}

    ExamFormSet = formset_factory(form_class, formset=BaseExamFormSet, extra=num_tests)
    if request.method == 'POST':
        formset = ExamFormSet(request.POST, form_kwargs={'tests': list(tests)})
        dict_answers = request.session.get('dict_answers') or {}
        if formset.is_valid():
            for form in formset:
                test = form.test
                answer = form.cleaned_data.get('answers')
                dict_answers[test.id] = answer
                if category_group == 1:
                    dict_part2_points[test.id] = answer
                elif answer in test.get_answers():
                    dict_correct_answers[test.id] = answer
            request.session['dict_part2_points'] = dict_part2_points
            request.session['dict_answers'] = dict_answers
            if category_group == 0:
                request.session['time'] = request.POST.get('time')
                request.session['dict_correct_answers'] = dict_correct_answers
                redirect_view = 'exam2' if tests_part2 else 'progress'
            else:
                redirect_view = 'progress'
            return redirect(redirect_view, variant_id=variant_id) if variant_id else redirect(redirect_view)
    else:
        formset = ExamFormSet(form_kwargs={'tests': list(tests)})
    return render(request, template_name, {'formset': formset})


def take_exam(request, variant_id=None):
    request.session['dict_answers'] = {}
    tests_part1, tests_part2 = get_tests(request, variant_id)
    tests = tests_part1 | tests_part2
    tests_count = (len(tests_part1), len(tests_part2))
    request.session['tests_count'] = tests_count
    num_tests = sum(tests_count)
    return handle_exam(request, tests, num_tests, EssayForm, 'exam/exam.html', variant_id, tests_part2,
                       category_group=0)


def take_exam2(request, variant_id=None):
    tests = get_tests(request, variant_id)[1]
    num_tests = request.session.get('tests_count')[1]
    return handle_exam(request, tests, num_tests, QuestionForm, 'exam/exam2.html', variant_id, tests_part2=None,
                       category_group=1)


def exam_filter(request):
    categories = Category.objects.prefetch_related('subcategory_set').all()
    num_cat = len(categories)
    FilterFormSet = formset_factory(form=FilterForm, formset=BaseFilterFormSet, extra=num_cat, max_num=num_cat,
                                    min_num=1, validate_min=True)
    tests_to_add = []
    if request.method == 'POST':
        formset = FilterFormSet(request.POST, form_kwargs={'categories': categories})
        if formset.is_valid():

            for form in formset:
                if form.has_changed():
                    cat_quantity = form.cleaned_data.get('cat_quantity')
                    subcategory = form.cleaned_data.get('subcategory')

                    if cat_quantity:
                        exercises = Exercise.objects.filter(subcategory__in=subcategory).order_by('?')[:cat_quantity]
                        tests = Test.objects.filter(exercise__in=exercises).all()
                        tests_to_add.extend(tests)

            request.session['tests_list'] = [test.id for test in tests_to_add]

            return redirect('exam')

    else:
        formset = FilterFormSet(form_kwargs={'categories': categories})

    return render(request, 'exam/exam_filter.html', {'formset': formset})


class ShowVariant(LoginRequiredMixin, ListView):
    template_name = 'exam/variants.html'
    context_object_name = 'variants'
    queryset = Exam.objects.filter(
        admin_created=True).all()
    print(queryset)

class ShowStatistics(ListView):
    template_name = 'exam/statistics.html'
    context_object_name = 'exam_attempts'
    extra_context = {'title': 'Статистика'}

    def get_queryset(self):
        exam_attempts = ExamAttempt.objects.filter(student=self.request.user).prefetch_related('exam__tests',
                                                                                               'question_attempts__test__exercise__subcategory',
                                                                                               'question_attempts__test__answer_set').annotate(
            tests_part2_count=Count(
                Case(
                    When(exam__tests__part2=True, then=1),
                    output_field=IntegerField()
                )
            ),
            tests_part1_count=Count(
                Case(
                    When(exam__tests__part2=False, then=1),
                    output_field=IntegerField()
                )
            ),
        )
        # exam_attempts = ExamAttempt.objects.filter(student=self.request.user).prefetch_related('question_attempts').all()
        return exam_attempts