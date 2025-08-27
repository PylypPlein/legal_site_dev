from django.shortcuts import render
from .models import Service
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactRequestForm
from .models import Employee, Firma, SocialLink, PrivacyPolicySection, PrivacyPolicySubsection, JobOffer, BlacklistedCountry,ServiceClass
from ipware import get_client_ip
# views.py
from django.shortcuts import render, redirect
from .forms import ContactRequestForm
from .models import Service
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactRequestForm
from .models import Service

def index(request):
    service_classes = ServiceClass.objects.prefetch_related("services").all()
    services = Service.objects.all()
    employees = Employee.objects.all()
    company = Firma.objects.first()
    links = SocialLink.objects.all()
    social_links = {link.name.lower(): link.url for link in links}
    google_data = get_google_reviews()

    print(google_data)
    return render(
        request,
        'main/index.html',
        {
            'services': services,
            'employees': employees,
            'company': company,
            'social_links': social_links,
            'isBlackListed': getattr(request, "is_blacklisted", False),
            'service_classes': service_classes,
        }
    )


def get_google_reviews():
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={settings.GOOGLE_MAPS_PLACE_ID}&"
        f"fields=reviews,name,rating,formatted_address&"
        f"key={settings.GOOGLE_MAPS_API}"
    )

    try:
        response = requests.get(url)
        print("URL:", url)
        print("STATUS:", response.status_code)
        print("JSON:", response.text)

        data = response.json()
        result = data.get("result", {})
        return {
            "name": result.get("name"),
            "address": result.get("formatted_address"),
            "rating": result.get("rating"),
            "reviews": result.get("reviews", []),
        }
    except Exception as e:
        print("Exception:", e)
        return {"name": None, "address": None, "rating": None, "reviews": []}



def privacy_policy(request):
    company = Firma.objects.first()
    sections = PrivacyPolicySection.objects.prefetch_related("subsections")
    return render(request, 'main/privacy_policy.html',{'company':company,"sections": sections})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()  # zapis do bazy

            # renderowanie szablonu HTML
            html_message = render_to_string(
                'main/emails/confirmation.html',
                {'contact': contact_instance, 'LANGUAGE_CODE': request.LANGUAGE_CODE}
            )

            email = EmailMessage(
                subject="Подтверждение записи на консультацию",
                body=html_message,
                from_email=None,  # używa DEFAULT_FROM_EMAIL
                to=[contact_instance.email],
            )
            email.content_subtype = "html"  # ważne, żeby wysyłać HTML
            email.send(fail_silently=False)

            messages.success(request, "Ваше сообщение отправлено и подтверждение выслано на email!")
            return redirect(reverse('index'))
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactRequestForm()

    services = Service.objects.all()
    return render(request, 'index.html', {'form': form, 'services': services})

'''
def contact(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение отправлено!")
            return redirect(reverse('index'))  # Можно изменить на страницу, куда хотите редиректить
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactRequestForm()

    services = Service.objects.all()
    return render(request, 'index.html', {'form': form, 'services': services})
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})
    

def job_list(request):
    jobs = JobOffer.objects.filter(status='published')
    company = Firma.objects.first()
    return render(request, 'main/job_offers.html', {'jobs': jobs,'company':company})
    '''
def job_list(request):
    # Pobranie danych do index.html (na wypadek zablokowanego)
    services = Service.objects.all()
    employees = Employee.objects.all()
    company = Firma.objects.first()
    links = SocialLink.objects.all()
    social_links = {link.name.lower(): link.url for link in links}

    # Sprawdzenie flagi z middleware
    is_blacklisted = getattr(request, "is_blacklisted", False)

    if is_blacklisted:
        # Renderujemy index.html zamiast job_offers.html
        return render(
            request,
            'main/index.html',
            {
                'services': services,
                'employees': employees,
                'company': company,
                'social_links': social_links,
                'isBlackListed': True
            }
        )

    # Jeśli nie zablokowany – normalny widok job_list
    jobs = JobOffer.objects.filter(status='published')
    company = Firma.objects.first()
    return render(request, 'main/job_offers.html', {'jobs': jobs, 'company': company})



def contact_view(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение отправлено!")
            return redirect(reverse('home'))  # Можно изменить на страницу, куда хотите редиректить
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactRequestForm()

    services = Service.objects.all()
    return render(request, 'contact_modal.html', {'form': form, 'services': services})

