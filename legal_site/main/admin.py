from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Service

from django.contrib import admin
from .models import Service, Employee, Firma, SocialLink, PrivacyPolicySection, PrivacyPolicySubsection

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_en', 'name_pl', 'name_ua')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position')

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = (
        'nazwa_firmy',
        'nip',
        'regon',
        'miasto',
        'telefon_administracja',
        'telefon_legalizacja',
        'email',
        'data_dodania',
    )
    search_fields = ('nazwa_firmy', 'nip', 'miasto', 'email')
    list_filter = ('miasto',)
    ordering = ('nazwa_firmy',)
    readonly_fields = ('data_dodania',)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

class PrivacyPolicySubsectionInline(admin.TabularInline):
    model = PrivacyPolicySubsection
    extra = 1

@admin.register(PrivacyPolicySection)
class PrivacyPolicySectionAdmin(admin.ModelAdmin):
    list_display = ("number", "title")
    inlines = [PrivacyPolicySubsectionInline]

@admin.register(PrivacyPolicySubsection)
class PrivacyPolicySubsectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "section")
    list_filter = ("section",)
