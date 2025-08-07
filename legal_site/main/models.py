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
