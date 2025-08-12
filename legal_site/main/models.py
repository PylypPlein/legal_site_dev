from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"


class Service(models.Model):
    name_pl = models.CharField("Название услуги (PL)", max_length=200)
    name_en = models.CharField("Название услуги (EN)", max_length=200)
    name_ru = models.CharField("Название услуги (RU)", max_length=200)
    name_ua = models.CharField("Название услуги (UA)", max_length=200)

    description_pl = models.TextField("Описание услуги (PL)")
    description_en = models.TextField("Описание услуги (EN)")
    description_ru = models.TextField("Описание услуги (RU)")
    description_ua = models.TextField("Описание услуги (UA)")

    def __str__(self):
        return self.name_pl

class Employee(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    photo = models.ImageField("Фото", upload_to='employees/')
    position = models.CharField("Вакансия", max_length=150)
    profession = models.CharField("Професия", max_length=150)
    age = models.PositiveIntegerField("Возраст")
    years_in_poland = models.PositiveIntegerField("Время перебывания в Польше")
    description = models.TextField("Описание")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models

class Firma(models.Model):
    nazwa_firmy = models.CharField(max_length=255, verbose_name="Nazwa firmy")
    nip = models.CharField(max_length=10, verbose_name="NIP")
    regon = models.CharField(max_length=9, blank=True, null=True, verbose_name="REGON")
    miasto = models.CharField(max_length=100, verbose_name="Miasto")
    adres = models.CharField(max_length=255, verbose_name="Adres")
    telefon_administracja = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon administracja")
    telefon_legalizacja = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon legalizacja")
    email = models.EmailField(verbose_name="Adres e-mail")
    data_dodania = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    def __str__(self):
        return self.nazwa_firmy

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"
        ordering = ['nazwa_firmy']


class SocialLink(models.Model):
    name = models.CharField("Назва платформи", max_length=100)
    url = models.URLField("Посилання")

    class Meta:
        verbose_name = "Соціальна мережа"
        verbose_name_plural = "Соціальні мережі"
        ordering = ['name']

    def __str__(self):
        return self.name


from django.db import models

class PrivacyPolicySection(models.Model):
    number = models.PositiveIntegerField(help_text="Numer sekcji, np. 1 dla §1")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"§{self.number} {self.title}"

class PrivacyPolicySubsection(models.Model):
    section = models.ForeignKey(PrivacyPolicySection, related_name="subsections", on_delete=models.CASCADE)
    number = models.PositiveIntegerField(help_text="Numer podsekcji wewnątrz sekcji, np. 1 dla 1.1")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.section.number}.{self.number}"

from django.db import models

class JobOffer(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Szkic'),
        ('published', 'Opublikowana'),
        ('closed', 'Zamknięta'),
    ]

    # Tytuł w różnych językach
    title_pl = models.CharField("Tytuł (PL)", max_length=200)
    title_en = models.CharField("Tytuł (EN)", max_length=200)
    title_ru = models.CharField("Tytuł (RU)", max_length=200)
    title_ua = models.CharField("Tytuł (UA)", max_length=200)

    # Nazwa firmy (zakładam, że nie trzeba tłumaczyć)
    company_name = models.CharField("Firma", max_length=150)

    location = models.CharField("Lokalizacja", max_length=150)

    # Opis stanowiska w różnych językach
    description_pl = models.TextField("Opis (PL)")
    description_en = models.TextField("Opis (EN)")
    description_ru = models.TextField("Opis (RU)")
    description_ua = models.TextField("Opis (UA)")

    # Wymagania w różnych językach
    requirements_pl = models.TextField("Wymagania (PL)", blank=True)
    requirements_en = models.TextField("Wymagania (EN)", blank=True)
    requirements_ru = models.TextField("Wymagania (RU)", blank=True)
    requirements_ua = models.TextField("Wymagania (UA)", blank=True)

    salary_from = models.DecimalField("Pensja od", max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField("Pensja do", max_digits=10, decimal_places=2, null=True, blank=True)

    published_at = models.DateTimeField("Data dodania", auto_now_add=True)
    valid_until = models.DateField("Oferta ważna do", null=True, blank=True)

    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = "Oferta pracy"
        verbose_name_plural = "Oferty pracy"
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title_pl} – {self.company_name}"
