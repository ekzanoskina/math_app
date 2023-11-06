from django import forms
from django.forms import BaseFormSet, ModelMultipleChoiceField, MultipleChoiceField, ChoiceField
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

    def __init__(self, category, subcategories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        self.fields['cat_quantity'].label = f"{category.number}. {category.title}"
        # self.fields['subcategory'].label = ''
        self.fields['subcategory'].queryset = subcategories

class BaseFilterFormSet(BaseFormSet):

    """
    FormSet with minimized number of SQL queries for ModelChoiceFields
    """

    def __init__( self, *args, modelchoicefields_qs=None, **kwargs ):
        """
        Overload the ModelChoiceField querysets by a common queryset per
        field, with dummy .all() and .iterator() methods to avoid multiple
        queries when filling the (repeated) choices fields.

        Parameters
        ----------

        modelchoicefields_qs :          dict
            Dictionary of modelchoicefield querysets. If ``None``, the
            modelchoicefields are identified internally

        """

        # Init the formset
        super(BaseFilterFormSet, self ).__init__( *args, **kwargs )

        if modelchoicefields_qs is None and len( self.forms ) > 0:
            # Store querysets of modelchoicefields
            modelchoicefields_qs = {}
            first_form = self.forms[0]
            for key in first_form.fields:
                if isinstance( first_form.fields[key], forms.ModelChoiceField ):
                    modelchoicefields_qs[key] = first_form.fields[key].queryset

        # Django calls .queryset.all() before iterating over the queried objects
        # to render the select boxes. This clones the querysets and multiplies
        # the queries for nothing.
        # Hence, overload the querysets' .all() method to avoid cloning querysets
        # in ModelChoiceField. Simply return the queryset itself with a lambda function.
        # Django also calls .queryset.iterator() as an optimization which
        # doesn't make sense for formsets. Hence, overload .iterator as well.
        if modelchoicefields_qs:
            for qs in modelchoicefields_qs.values():
                qs.all = lambda local_qs=qs: local_qs  # use a default value of qs to pass from late to immediate binding (so that the last qs is not used for all lambda's)
                qs.iterator = qs.all

            # Apply the common (non-cloning) querysets to all the forms
            for form in self.forms:
                for key in modelchoicefields_qs:
                    form.fields[key].queryset = modelchoicefields_qs[key]
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        cat = kwargs['categories'][index]
        subcats = kwargs['dict_categories'][cat]
        return {'category': cat, 'subcategories': subcats}
    def full_clean(self):
        super(BaseFilterFormSet, self).full_clean()

        for error in self._non_form_errors.as_data():
            if error.code == 'too_few_forms':
                error.message = "Пожалуйста, выберете хотя бы %d тип." % self.min_num