import requests
from ipware import get_client_ip
from django.shortcuts import render
from .models import BlacklistedCountry

class LogUserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "Не удалось определить IP"

        country = "Неизвестно"
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}").json()
            country = response.get("country", "None")
        except Exception:
            pass

        # Логируем в консоль
        print(f"[User visit] IP: {ip} | Country: {country}")

        # sprawdzamy w bazie
        request.is_blacklisted = BlacklistedCountry.objects.filter(
            name__iexact=country
        ).exists()

        return self.get_response(request)

