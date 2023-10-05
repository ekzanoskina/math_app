from django import forms
from django.forms import BaseFormSet, ModelMultipleChoiceField
from django.forms import BaseModelFormSet
from django.forms.widgets import Textarea
from math_app.models import *
from .models import *
from django.forms.widgets import RadioSelect

CHOICE_LIST = [
    ("0", 0),
    ("1", 1),
    ("2", 2),
]
class QuestionForm(forms.Form):
    answers = forms.ChoiceField(choices=CHOICE_LIST, widget=forms.RadioSelect(), label="Укажите набранное количество баллов:", required=False)
    def __init__(self, test, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.test = test


class EssayForm(forms.Form):
    def __init__(self, test, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.test = test
        self.fields["answers"] = forms.CharField(required=False, initial='')
        self.fields['answers'].label = 'Ответ'
class BaseExamFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        test = kwargs['tests'][index]
        return {'test': test}

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.title}"
class FilterForm(forms.Form):
    cat_quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'placeholder':0, 'class':"cat_quantity"}), required = False)
    subcategory = MyModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(attrs={'class':"check"}), required = False)
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        self.fields['cat_quantity'].label = f"{category.number}. {category.title}"
        self.fields['subcategory'].label = ''
        self.fields['subcategory'].queryset = Subcategory.objects.filter(category__title=category.title)

class BaseFilterFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        cat = kwargs['categories'][index]
        print(index)
        return {'category': cat}
    def full_clean(self):
        super(BaseFilterFormSet, self).full_clean()

        for error in self._non_form_errors.as_data():
            if error.code == 'too_few_forms':
                error.message = "Пожалуйста, выберете хотя бы %d тип." % self.min_num