from django.contrib import admin
from .models import Variant

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['pk']
