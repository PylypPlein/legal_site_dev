from django.contrib import admin
from .models import Service, Employee, Firma, SocialLink, PrivacyPolicySection, PrivacyPolicySubsection
from .models import JobOffer
from .models import BlacklistedCountry, ContactRequest, Service

from django.contrib import admin
from .models import ServiceClass, Service


@admin.register(ServiceClass)
class ServiceClassAdmin(admin.ModelAdmin):
    list_display = ("id", "name_pl", "name_en", "name_ru", "name_ua", "name_es")
    search_fields = ("name_pl", "name_en", "name_ru", "name_ua", "name_es")
    list_filter = ("name_pl",)  # możesz filtrować po polskiej nazwie
    ordering = ("id",)
    # fields określa kolejność w formularzu edycji
    fields = (
        "name_pl", "name_en", "name_ru", "name_ua", "name_es",
        "description_pl", "description_en", "description_ru",
        "description_ua", "description_es",
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name_pl", "service_class")
    list_filter = ("service_class",)
    search_fields = ("name_pl", "name_en", "name_ru", "name_ua", "name_es")
    ordering = ("id",)


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



@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title_pl", "company_name", "location", "status", "published_at", "valid_until")
    list_filter = ("status", "location", "company_name")
    search_fields = ("title_pl", "title_en", "title_ru", "title_ua",
                     "description_pl", "description_en", "description_ru", "description_ua")
    ordering = ("-published_at",)
    date_hierarchy = "published_at"
    list_editable = ("status",)

    fieldsets = (
        ("Podstawowe informacje", {
            "fields": ("company_name", "location", "status", "salary_from", "salary_to", "valid_until")
        }),
        ("Tytuł w różnych językach", {
            "fields": ("title_pl", "title_en", "title_ru", "title_ua")
        }),
        ("Opis w różnych językach", {
            "fields": ("description_pl", "description_en", "description_ru", "description_ua")
        }),
        ("Wymagania w różnych językach", {
            "fields": ("requirements_pl", "requirements_en", "requirements_ru", "requirements_ua")
        }),
    )

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(BlacklistedCountry)
class BlacklistedCountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
