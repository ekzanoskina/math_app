from django.urls import path
from .views import *

urlpatterns = [
    path('filter', exam_filter, name='exam_filter'),
    # path('exam/<int:variant_id>', take_exam, name='exam'),
    # path('exam2/<int:variant_id>', take_exam2, name='exam2'),
    path('progress/<int:variant_id>', show_progress, name='progress'),
    path('variants/', ShowVariant.as_view(), name='variants'),
    path('test_exam/', ExamWizard.as_view(FORMS, condition_dict={'exam2': part2}), name='test_exam'),
    path('test_exam/<int:variant_id>', ExamWizard.as_view(FORMS, condition_dict={'exam2': part2}), name='test_exam'),
    # path('<slug:subcat_slug>/', show_subcategory, name='subcategory'),
    # path('exercise/<int:ex_id>/', show_exercise, name='exercise'),


]