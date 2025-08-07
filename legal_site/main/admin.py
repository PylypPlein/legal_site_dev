from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Service

from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_en', 'name_pl', 'name_ua')

