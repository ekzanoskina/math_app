from django.contrib.messages.storage import session
from django.forms import formset_factory
from django.db.models import Q
from math_app.models import *
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView, ListView
from formtools.wizard.views import SessionWizardView


def show_progress(request, variant_id):
    if variant_id:
        variant = Variant.objects.get(pk=variant_id)
        tests_part1 = Test.objects.filter(
            Q(exercise__in=variant.exercise.all()) & Q(exercise__subcategory__category__id__lt=20))
        tests_part2 = Test.objects.filter(
            Q(exercise__in=variant.exercise.all()) & Q(exercise__subcategory__category__id__gt=19))

    else:
        tests_part1 = Test.objects.filter(
            Q(exercise__id__in=request.session['exercises_list']) & Q(exercise__subcategory__category__id__lt=20))
        tests_part2 = Test.objects.filter(
            Q(exercise__id__in=request.session['exercises_list']) & Q(exercise__subcategory__category__id__gt=19))
    tests = tests_part1 | tests_part2
    answers = request.session.get('dict_answers')
    correct_answers = request.session.get('dict_correct_answers')
    dict_part2_points = request.session.get('dict_part2_points')
    time = request.session.get('time')
    max_result = tests_part1.count() + (tests_part2.count() * 2)
    result = len(correct_answers)
    geometry_result = len([val for key, val in correct_answers.items() if
                           Test.objects.get(id=key).get_category_id() in [15, 16, 17, 18, 19]])
    if len(dict_part2_points) > 0:
        result += sum([int(point) for point in dict_part2_points.values() if point != None])
        geometry_result += sum([int(val) for key, val in dict_part2_points.items() if
                                Test.objects.get(id=key).get_category_id() in [23, 24, 25] and val != None])
    mark = '2'
    if geometry_result >= 2:
        if 8 <= result < 15:
            mark = '3'
        elif 15 <= result < 22:
            mark = '4'
        elif result >= 22:
            mark = '5'
    return render(request, 'exam/progress.html',
                  {'variant_id': variant_id, 'tests': tests, 'tests_part1': tests_part1, 'tests_part2': tests_part2,
                   'correct_answers': correct_answers, 'answers': answers, 'time': time, 'max_result': max_result,
                   'result': result, 'geometry_result': geometry_result, 'mark': mark})

#
def exam_filter(request):
    categories = Category.objects.all()
    num_cat = categories.count()
    lst = []
    FilterFormSet = formset_factory(form=FilterForm, formset=BaseFilterFormSet, extra=num_cat, max_num=num_cat,
                                    min_num=1, validate_min=True)
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
            return redirect('test_exam')

    else:
        formset = FilterFormSet(form_kwargs={'categories': list(categories), })
    return render(request, 'exam/exam_filter.html', {'formset': formset})


class ShowVariant(ListView):
    model = Variant
    template_name = 'exam/variants.html'
    context_object_name = 'variants'


EssayFormSet = formset_factory(form=EssayForm, formset=BaseExamFormSet)
RadioButtonFormSet = formset_factory(form=QuestionForm, formset=BaseExam2FormSet)

FORMS = [("exam", EssayFormSet),
         ("exam2", RadioButtonFormSet)]

TEMPLATES = {"exam": "exam/exam_test.html",
             "exam2": "exam/exam2_test.html"}


def part2(wizard):
    all_tests = Test.objects.filter(exercise__in=wizard.request.session.get('exercises_list')).order_by(
        'exercise__subcategory__category__id')
    return all_tests.filter(exercise__subcategory__category__id__gt=19).count() > 0


class ExamWizard(SessionWizardView):

    def get_test_answers(self, form_obj):
        my_dict = {}

        for form in form_obj:
            if hasattr(form, 'test'):
                my_dict[form.test] = form.cleaned_data.get('answers', '')
            else:
                my_dict[form.test_part2] = form.cleaned_data.get('answers', '')

        return my_dict

    def get_all_cleaned_data(self):
        """
        Returns a merged dictionary of all step cleaned_data dictionaries.
        If a step contains a `FormSet`, the key will be prefixed with
        'formset-' and contain a list of the formset cleaned_data dictionaries.
        """
        cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    cleaned_data.update({
                        'formset-%s' % form_key: self.get_test_answers(form_obj)
                    })
                else:
                    cleaned_data.update(form_obj.cleaned_data)
        return cleaned_data

    def done(self, form_list, **kwargs):
        formset_dict = self.get_all_cleaned_data()
        formset_1 = formset_dict.get('formset-exam')
        formset_2 = formset_dict.get('formset-exam2')
        answers = {test.id:ans for test, ans in formset_1.items()}
        print(answers)
        time = self.storage.get_step_data('exam').get('time')
        context = self.get_context_data('exam')
        tests = context['all_tests']
        print(tests)
        variant_id = context.get('variant_id')
        tests_part1 = context['tests_part1']
        tests_part2 = context['tests_part2']
        max_result = 0

        correct_answers = {test: ans for test, ans in formset_1.items() if ans in test.get_answers()}


        result = len(correct_answers)
        geometry_result = len([ans for test, ans in correct_answers.items() if
                               Test.objects.get(id=test.id).get_category_id() in [15, 16, 17, 18, 19]])
        if formset_2:
            dict_part2_points = {test.id:ans for test, ans in formset_2.items()}
            answers.update(dict_part2_points)
            print(dict_part2_points)
            result += sum([int(point) for point in dict_part2_points.values() if point != None])
            geometry_result += sum([int(val) for key, val in dict_part2_points.items() if
                                    Test.objects.get(id=key).get_category_id() in [23, 24, 25] and val != None])

        mark = '2'
        if geometry_result >= 2:
            if 8 <= result < 15:
                mark = '3'
            elif 15 <= result < 22:
                mark = '4'
            elif result >= 22:
                mark = '5'
        #
        return render(self.request, 'exam/progress.html',
                      {'variant_id': variant_id, 'tests': tests, 'tests_part1': tests_part1, 'tests_part2': tests_part2,
                       'correct_answers': correct_answers, 'answers': answers, 'time': time, 'max_result': max_result,
                       'result': result, 'geometry_result': geometry_result, 'mark': mark}
                      )

    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super(ExamWizard, self).get_context_data(form, **kwargs)
        variant_id = self.kwargs.get('variant_id', False)
        if variant_id:
            variant = Variant.objects.get(pk=variant_id)
            all_tests = Test.objects.filter(exercise__in=variant.exercise.all()).order_by(
                'exercise__subcategory__category__id')
            context.update({'variant_id': variant_id})
        else:
            all_tests = Test.objects.filter(exercise__in=self.request.session.get('exercises_list')).order_by(
                'exercise__subcategory__category__id')
        tests_part1 = all_tests.filter(exercise__subcategory__category__id__lt=20).order_by(
                'exercise__subcategory__category__id')
        tests_part2 = all_tests.filter(exercise__subcategory__category__id__gt=19).order_by(
                'exercise__subcategory__category__id')
        context.update({'all_tests': all_tests})
        context.update({'tests_part2': tests_part2})
        context.update({'tests_part1': tests_part1})
        return context



    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step is None:
            step = self.steps.current

        context = self.get_context_data(step)
        all_tests = context['all_tests']

        if step == 'exam':
            num_tests = all_tests.count()
            EssayFormSet = formset_factory(form=EssayForm, formset=BaseExamFormSet, extra=num_tests)
            form = EssayFormSet(data, form_kwargs={'tests': all_tests})


        elif step == 'exam2':
            tests_part2 = all_tests.filter(exercise__subcategory__category__id__gt=19).order_by(
                'exercise__subcategory__category__id')
            num_tests_part2 = tests_part2.count()
            RadioButtonFormSet = formset_factory(form=QuestionForm, formset=BaseExam2FormSet, extra=num_tests_part2)
            form = RadioButtonFormSet(data, form_kwargs={'tests_part2': tests_part2})

        return form


