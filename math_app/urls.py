from django.urls import path, include
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('subcategory/<slug:subcat_slug>/', ShowSubcategory.as_view(), name='subcategory'),
    path('test/<int:test_id>/', ShowTest.as_view(), name='test'),

]