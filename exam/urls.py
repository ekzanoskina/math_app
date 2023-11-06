from django.urls import path, include
from .views import *

urlpatterns = [
    path('filter', exam_filter, name='exam_filter'),
    path('exam/', take_exam, name='exam'),
    path('exam/<int:variant_id>', take_exam, name='exam'),
    path('exam2/', take_exam2, name='exam2'),
    path('exam2/<int:variant_id>', take_exam2, name='exam2'),
    path('progress/', show_progress, name='progress'),
    path('progress/<int:variant_id>', show_progress, name='progress'),
    path('variants/', ShowVariant.as_view(), name='variants')
    # path('<slug:subcat_slug>/', show_subcategory, name='subcategory'),
    # path('exercise/<int:ex_id>/', show_exercise, name='exercise'),

]